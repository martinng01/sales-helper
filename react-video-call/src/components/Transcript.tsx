import { useEffect } from "react";
import { socket } from "../socket";

const Transcript = () => {
  useEffect(() => {
    //TODO: Transcript
    socket.on("transcript", (data) => {
      console.log(data);
    });
  }, []);

  return <></>;
};

export default Transcript;
