import { DefaultEventsMap } from "@socket.io/component-emitter";
import io, { Socket } from "socket.io-client";

let socket: Socket<DefaultEventsMap, DefaultEventsMap>;
const connectSocket = () => {
  if (!socket) {
    socket = io("http://localhost:8765", {
      transports: ["websocket", "polling"],
    });

    socket.on("connect", () => {
      console.log("Socket connected:", socket.id);
    });

    socket.on("disconnect", (reason) => {
      console.log("Socket disconnected:", reason);
      if (reason === "io server disconnect") {
        // The disconnection was initiated by the server, reconnect manually
        socket.connect();
      }
    });

    socket.on("connect_error", (error) => {
      console.error("Socket connection error:", error);
      // Try to reconnect after a delay
      setTimeout(() => socket.connect(), 5000);
    });
  }
};

connectSocket();

// Now you can use the socket object for emitting events
export { socket };
