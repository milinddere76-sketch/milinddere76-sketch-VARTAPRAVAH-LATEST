# Varta Pravah - Broadcast Grade Playout Engine
# Powered by Liquidsoap

set("log.file", false)
set("log.stdout", true)
set("server.telnet", true)

# 1. SOURCE: News Bulletins
# Automatically watches the directory for new .mp4 files from Hetzner
news = playlist(reload_mode="watch", "/app/videos")

# 2. SOURCE: Branded Promos / Fillers
promo = single("/app/assets/promo.mp4")

# 3. LOGIC: Playout Sequence
# Plays one news bulletin, then one promo. 
# This ensures a "Promo after story ends" flow and approximates the 5-min interval.
broadcast = rotate(weights=[1, 1], [news, promo])

# 4. SECURITY: Fallback
# If no news is available, stay on the promo loop 24/7
broadcast = fallback(track_sensitive=false, [broadcast, promo])

# 5. OUTPUT: Stream to local NGINX RTMP Relay
# NGINX will then handle the stable push to YouTube
output.rtmp(
  host="localhost",
  port=1935,
  app="live",
  stream="stream",
  broadcast
)
