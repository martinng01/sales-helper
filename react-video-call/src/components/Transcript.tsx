import { useEffect, useState } from "react";
import { socket } from "../socket";

const Transcript = () => {
  const [transcript, setTranscript] = useState<string>("");

  useEffect(() => {
    socket.on("transcript", (text) => {
      setTranscript(text);
    });
  }, []);

  if (!transcript) {
    return null;
  }

  return (
    <div className="absolute bottom-8 left-4 right-4 max-w-4xl mx-auto p-4 bg-white/60 backdrop-blur-lg rounded-lg shadow-lg">
      <p className="text-gray-800">{transcript}</p>
    </div>
  );
};

export default Transcript;
