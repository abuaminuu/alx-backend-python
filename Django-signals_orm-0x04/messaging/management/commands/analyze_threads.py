from django.core.management.base import BaseCommand
from django.db.models import Count, Avg
from messaging.models import Message

class Command(BaseCommand):
    help = 'Analyze threaded conversation patterns and performance'
    
    def handle(self, *args, **options):
        """
        Create Management Command for Thread Analysis
        Analyze thread patterns and ORM performance
        """
        
        # Thread statistics
        thread_starters = Message.objects.filter(is_thread_starter=True)
        self.stdout.write(f"Total thread starters: {thread_starters.count()}")
        
        # Average replies per thread
        avg_replies = thread_starters.annotate(
            reply_count=Count('replies')
        ).aggregate(avg=Avg('reply_count'))['avg'] or 0
        
        self.stdout.write(f"Average replies per thread: {avg_replies:.2f}")
        
        # Thread depth analysis
        max_depth = Message.objects.aggregate(max_depth=Avg('thread_depth'))['max_depth'] or 0
        self.stdout.write(f"Average thread depth: {max_depth:.2f}")
        
        # Most active threads
        active_threads = thread_starters.annotate(
            total_messages=Count('replies') + 1  # +1 for starter
        ).order_by('-total_messages')[:5]
        
        self.stdout.write("\nMost active threads:")
        for thread in active_threads:
            self.stdout.write(
                f"  Thread {thread.id}: {thread.total_messages} messages "
                f"(started by {thread.sender.username})"
            )
        
        # Query optimization analysis
        self.stdout.write("\nQuery Optimization Analysis:")
        
        # Test select_related performance
        import time
        start_time = time.time()
        
        # Without optimization
        messages = Message.objects.all()[:10]
        for msg in messages:
            _ = msg.sender.username
            _ = msg.receiver.username
        
        time_without_opt = time.time() - start_time
        
        # With optimization
        start_time = time.time()
        messages = Message.objects.select_related('sender', 'receiver')[:10]
        for msg in messages:
            _ = msg.sender.username
            _ = msg.receiver.username
        
        time_with_opt = time.time() - start_time
        
        self.stdout.write(f"Time without select_related: {time_without_opt:.4f}s")
        self.stdout.write(f"Time with select_related: {time_with_opt:.4f}s")
        self.stdout.write(f"Optimization improvement: {((time_without_opt - time_with_opt) / time_without_opt * 100):.1f}%")
