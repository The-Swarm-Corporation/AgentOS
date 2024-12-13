mkdir -p data logs
chmod 770 data logs
docker compose up -d
docker compose logs -f
# docker compose down