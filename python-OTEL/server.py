import logging
import os
from fastapi import FastAPI, HTTPException, Request
from opentelemetry import _logs, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configuration
OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
SERVICE_NAME = os.getenv("CONTAINER_APP_NAME", "python-api")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")

def setup_telemetry():
    """Configure OpenTelemetry for both logs and traces"""
    
    # Create resource with service information
    resource = Resource.create({
        "service.name": SERVICE_NAME,
        "service.version": SERVICE_VERSION,
        "service.instance.id": os.getenv("HOSTNAME", "localhost"),
    })
    
    # === LOGS SETUP ===
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    
    # Create OTLP log exporter
    log_exporter = OTLPLogExporter(
        endpoint=OTEL_ENDPOINT,
        headers={},
        timeout=30,
    )
    
    # Add batch processor for logs
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(log_exporter)
    )
    
    # Configure Python logging to use OpenTelemetry
    # This handler will send Python logs as OTEL logs (not traces)
    otel_handler = LoggingHandler(logger_provider=logger_provider)
    otel_handler.setLevel(logging.INFO)
    
    # === TRACES SETUP ===
    trace_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(trace_provider)
    
    # Create OTLP trace exporter
    trace_exporter = OTLPSpanExporter(
        endpoint=OTEL_ENDPOINT,
        headers={},
        timeout=30,
    )
    
    # Add batch processor for traces
    trace_provider.add_span_processor(
        BatchSpanProcessor(trace_exporter)
    )
    
    # Get tracer for manual span creation
    tracer = trace.get_tracer(__name__)
    
    return otel_handler, tracer

# otel_logger = setup_logging()

# Initialize OpenTelemetry
otel_handler, tracer = setup_telemetry()


app = FastAPI(title="OTEL Example", version="1.0.0")

FastAPIInstrumentor.instrument_app(app)

# Configure loggers
# Logger for business/application logs (will be sent as LOGS)
app_logger = logging.getLogger("app")
app_logger.setLevel(logging.INFO)
app_logger.addHandler(otel_handler)

# Logger for audit events (will be sent as LOGS)
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)
audit_logger.addHandler(otel_handler)

# Logger for security events (will be sent as LOGS)
security_logger = logging.getLogger("security")
security_logger.setLevel(logging.INFO)
security_logger.addHandler(otel_handler)


@app.on_event("startup")
async def startup_event():
    app_logger.info("Application starting up", extra={
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "event": "startup",
    })

@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("Application shutting down", extra={
        "service": SERVICE_NAME,
        "event": "shutdown",
    })

@app.get("/")
async def root():
    app_logger.info("Root endpoint accessed", extra={
        "endpoint": "/",
        "method": "GET",
    })
    return {"message": "Hello World!"}

@app.get("/status")
async def get_status():
    app_logger.info("status endpoint accessed", extra={
        "endpoint": "/status",
        "method": "GET",
        "status": "healthy",
    })
    return {"status": "healthy"}

@app.get("/location")
async def get_location():
    location = os.getenv('LOCATION', "not_set")
    app_logger.info("location endpoint accessed", extra={
        "endpoint": "/location",
        "method": "GET",
        "location": location,
    })
    return {"location": location}

@app.get("/headers")
async def get_headers(request: Request):
    app_logger.info("headers endpoint accessed", extra={
        "endpoint": "/headers",
        "method": "GET",
        "headers": dict(request.headers),
    })
    return {"headers": dict(request.headers)}

@app.post("/body")
async def get_body(request: Request):
    body = await request.body()
    body_str = body.decode('utf-8') if body else ""
    
    app_logger.info("v endpoint accessed", extra={
        "endpoint": "/body",
        "method": "GET",
        "body": body_str,
    })

    return {"body": body_str}

@app.get("/error")
async def error_demo():
    app_logger.error("Demonstrating error logging", extra={
        "endpoint": "/error",
        "error_type": "demonstration",
        "severity": "high"
    })
    
    try:
        # Simulate an error
        result = 1 / 0
    except Exception as e:
        app_logger.exception("Division by zero error occurred", extra={
            "error_type": "ZeroDivisionError",
            "operation": "division"
        })
        raise HTTPException(status_code=500, detail="Internal server error")
