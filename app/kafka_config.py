import asyncio
import json
import logging
from typing import Dict, Any, Optional
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from .config import settings

logger = logging.getLogger(__name__)

class KafkaProducer:
    def __init__(self):
        self.producer: Optional[AIOKafkaProducer] = None
        self.is_connected = False
        
    async def connect(self):
        """Connect to Kafka broker"""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                retries=3,
                acks='all'
            )
            await self.producer.start()
            self.is_connected = True
            logger.info("Connected to Kafka broker")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            self.is_connected = False
            
    async def disconnect(self):
        """Disconnect from Kafka broker"""
        if self.producer and self.is_connected:
            try:
                await self.producer.stop()
                self.is_connected = False
                logger.info("Disconnected from Kafka broker")
            except Exception as e:
                logger.error(f"Error disconnecting from Kafka: {e}")
                
    async def send_analytics_event(self, event_type: str, data: Dict[str, Any], user_id: Optional[int] = None):
        """Send analytics event to Kafka"""
        if not self.is_connected:
            logger.warning("Kafka not connected, skipping analytics event")
            return
            
        try:
            event = {
                "event_type": event_type,
                "timestamp": data.get("timestamp"),
                "user_id": user_id,
                "data": data
            }
            
            # Send to analytics topic
            await self.producer.send_and_wait(
                topic=settings.kafka_analytics_topic,
                key=f"analytics_{event_type}",
                value=event
            )
            
            logger.info(f"Analytics event sent: {event_type}")
            
        except KafkaError as e:
            logger.error(f"Failed to send analytics event: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending analytics event: {e}")
            
    async def send_product_event(self, event_type: str, product_data: Dict[str, Any], user_id: Optional[int] = None):
        """Send product-related analytics event"""
        await self.send_analytics_event(
            event_type=event_type,
            data={
                "product_id": product_data.get("id"),
                "product_name": product_data.get("name"),
                "price": product_data.get("price"),
                "category": product_data.get("category"),
                "timestamp": product_data.get("created_at")
            },
            user_id=user_id
        )
        
    async def send_order_event(self, event_type: str, order_data: Dict[str, Any], user_id: Optional[int] = None):
        """Send order-related analytics event"""
        await self.send_analytics_event(
            event_type=event_type,
            data={
                "order_id": order_data.get("id"),
                "total_amount": order_data.get("total_amount"),
                "item_count": order_data.get("item_count", 0),
                "timestamp": order_data.get("created_at")
            },
            user_id=user_id
        )
        
    async def send_user_event(self, event_type: str, user_data: Dict[str, Any], user_id: Optional[int] = None):
        """Send user-related analytics event"""
        await self.send_analytics_event(
            event_type=event_type,
            data={
                "user_id": user_id,
                "user_role": user_data.get("role"),
                "timestamp": user_data.get("created_at")
            },
            user_id=user_id
        )

# Global Kafka producer instance
kafka_producer = KafkaProducer()

async def get_kafka_producer() -> KafkaProducer:
    """Dependency to get Kafka producer"""
    if not kafka_producer.is_connected:
        await kafka_producer.connect()
    return kafka_producer
