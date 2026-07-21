import psutil
import time
import threading
from voice_output import VoiceOutput

class SystemMonitor:
    """Proactively monitors the system and alerts the user of anomalies."""
    
    def __init__(self, voice_module: VoiceOutput):
        self.voice = voice_module
        self.running = False
        self.monitor_thread = None

    def start(self):
        """Starts the background monitoring thread."""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            print("[*] Proactive System Monitor started.")

    def stop(self):
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)

    def _monitor_loop(self):
        # We don't want it to spam, so we keep track of when we last warned
        last_cpu_warning = 0
        while self.running:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                
                # If CPU is consistently over 90% and we haven't warned in 60 seconds
                if cpu_percent > 90.0 and (time.time() - last_cpu_warning) > 60:
                    print(f"\n[!] ALERT: High CPU Usage detected ({cpu_percent}%)")
                    # Unprompted voice alert
                    self.voice.speak(f"Warning. The system CPU usage has spiked to {int(cpu_percent)} percent.")
                    last_cpu_warning = time.time()
                
                time.sleep(5) # Check every 5 seconds
            except Exception as e:
                print(f"[-] Monitor error: {e}")
                time.sleep(10)

if __name__ == "__main__":
    from voice_output import VoiceOutput
    vo = VoiceOutput(use_edge=False)
    mon = SystemMonitor(vo)
    mon.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mon.stop()
