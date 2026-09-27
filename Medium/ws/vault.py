import asyncio
import base64
import json
import websockets

ENCODED_FLAG = "<flag>"


async def handle_client(websocket):
  print("[+] Client connected to local vault node.")

  try:
    # Send welcome broadcast
    welcome_msg = {
        "status": "ONLINE",
        "system": "Sector 21 Vault Telemetry",
        "notice": "Access Restricted. Send command JSON to authenticate.",
    }
    await websocket.send(json.dumps(welcome_msg))

    async for message in websocket:
      try:
        data = json.loads(message)
        if data.get("COMMAND") == "OVERRIDE":
          # Decode Base64 string dynamically
          flag = base64.b64decode(ENCODED_FLAG).decode("utf-8")
          response = {
              "status": "GRANTED",
              "message": "Vault Unlocked!",
              "flag": flag,
          }
          await websocket.send(json.dumps(response))
        else:
          await websocket.send(
              json.dumps({"status": "DENIED", "message": "Invalid Command."})
          )
      except json.JSONDecodeError:
        await websocket.send(
            json.dumps({"status": "ERROR", "message": "Malformed JSON."})
        )

  except websockets.exceptions.ConnectionClosed:
    print("[-] Client disconnected.")


async def main():
  print("=" * 50)
  print("[SECTOR 21] Local WebSocket Vault Server Running...")
  print("Listening on ws://127.0.0.1:8765")
  print("Keep this terminal open while solving the challenge!")
  print("=" * 50)

  async with websockets.serve(handle_client, "127.0.0.1", 8765):
    await asyncio.Future()  # Keep server running


if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print("\n[!] Server stopped.")