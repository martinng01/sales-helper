import { useEffect, useState } from "react";
import { socket } from "../socket";

const Emotion = () => {
  const [emotion, setEmotion] = useState<string>("🫥");

  useEffect(() => {
    socket.on("emotion", (text) => {
      console.log(text);
      setEmotion(text);
    });
  }, []);

  return <div className="absolute top-0 right-0 m-4 text-6xl">{emotion}</div>;
};

export default Emotion;
