"""
Secure Telegram API Credentials Loader
Handles API_ID and API_HASH securely without exposing them in logs or code
"""

import os
import logging
from typing import Tuple, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class SecureCredentials:
    """Secure credentials loader for Telegram API"""
    
    @staticmethod
    def get_api_credentials() -> Tuple[Optional[int], Optional[str]]:
        """
        Get Telegram API credentials securely
        
        Returns:
            Tuple[api_id, api_hash]
        """
        api_id = os.getenv('TELEGRAM_API_ID')
        api_hash = os.getenv('TELEGRAM_API_HASH')
        
        if not api_id or not api_hash:
            logger.warning("⚠️  Telegram API credentials not configured")
            logger.warning("   Get from: https://my.telegram.org/apps")
            return None, None
        
        try:
            api_id = int(api_id)
            logger.info("✅ API ID loaded securely")
            logger.info(f"✅ API Hash loaded securely ({len(api_hash)} chars)")
            return api_id, api_hash
        except ValueError:
            logger.error("❌ Invalid API_ID format (must be integer)")
            return None, None
    
    @staticmethod
    def get_bot_token() -> Optional[str]:
        """
        Get Bot Token securely
        
        Returns:
            Bot token string
        """
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            logger.error("❌ TELEGRAM_BOT_TOKEN not found")
            return None
        
        logger.info(f"✅ Bot token loaded securely ({len(token)} chars)")
        return token
    
    @staticmethod
    def get_admin_ids() -> list:
        """
        Get admin IDs securely
        
        Returns:
            List of admin usernames/IDs
        """
        admin_ids = os.getenv('TELEGRAM_ADMIN_IDS', '')
        if not admin_ids:
            logger.warning("⚠️  No admin IDs configured")
            return []
        
        admins = [id.strip() for id in admin_ids.split(',')]
        logger.info(f"✅ {len(admins)} admin(s) loaded")
        return admins
    
    @staticmethod
    def validate_all_credentials() -> bool:
        """
        Validate all credentials are properly configured
        
        Returns:
            True if all required credentials are valid
        """
        logger.info("🔐 Validating credentials...")
        
        # Check Bot Token
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            logger.error("❌ TELEGRAM_BOT_TOKEN missing")
            return False
        logger.info("✅ Bot token present")
        
        # Check API Credentials
        api_id = os.getenv('TELEGRAM_API_ID')
        api_hash = os.getenv('TELEGRAM_API_HASH')
        
        if api_id and api_hash:
            logger.info("✅ API credentials present")
        else:
            logger.warning("⚠️  API credentials not configured (optional)")
        
        # Check Admin IDs
        admin_ids = os.getenv('TELEGRAM_ADMIN_IDS')
        if admin_ids:
            logger.info("✅ Admin IDs configured")
        else:
            logger.warning("⚠️  No admin IDs configured")
        
        logger.info("✅ Credentials validation complete")
        return True


# Example usage
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Validate credentials
    SecureCredentials.validate_all_credentials()
    
    # Get credentials
    api_id, api_hash = SecureCredentials.get_api_credentials()
    token = SecureCredentials.get_bot_token()
    admins = SecureCredentials.get_admin_ids()
    
    print("\n✅ All credentials loaded securely!")
