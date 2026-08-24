from datetime import date, datetime
import logging
from src.services.BookingTicketService import BookingTicketService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('booking_crawler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """主程序入點"""
    try:
        # 取得今天的日期
        today = date.today()
        logger.info(f"開始處理日期 {today} 的訂票")
        
        # 初始化訂票服務
        booking_service = BookingTicketService()
        
        # 處理訂票
        successful_count, failed_count = booking_service.process_daily_bookings(today)
        
        # 記錄結果
        logger.info(f"訂票完成 - 成功: {successful_count}, 失敗: {failed_count}")
        
        return successful_count, failed_count
    
    except Exception as e:
        logger.error(f"訂票過程中發生錯誤: {str(e)}", exc_info=True)
        return 0, -1


if __name__ == "__main__":
    main()
