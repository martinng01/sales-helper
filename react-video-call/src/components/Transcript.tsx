import { useEffect, useState } from "react";
import { socket } from "../socket";

const Transcript = () => {
  const [transcript, setTranscript] = useState<string>(
    `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur`
  );

  useEffect(() => {
    socket.on("transcript", (data) => {
      console.log(data);
      setTranscript(data.transcript);
    });
  }, []);

  return (
    <div className="absolute bottom-8 left-4 right-4 max-w-4xl mx-auto p-4 bg-white/60 backdrop-blur-lg rounded-lg shadow-lg">
      <p className="text-gray-800">{transcript}</p>
    </div>
  );
};

export default Transcript;
