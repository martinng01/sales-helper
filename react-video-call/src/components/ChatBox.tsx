import { useEffect, useState } from "react";
import { RxCross1 } from "react-icons/rx";
import { socket } from "../socket";

interface MessageType {
  id: number;
  text: string;
}

const ChatBox = () => {
  const [messages, setMessages] = useState<MessageType[]>([]);

  const deleteMessage = (id: number) => {
    setMessages(messages.filter((message) => message.id !== id));
  };

  useEffect(() => {
    const addMessage = (message: MessageType) => {
      setMessages([...messages, message]);
    };

    //TODO: Segments?
    socket.on("segments", (data) => {
      const message: MessageType = {
        id: Math.random(),
        text: data.message,
      };
      addMessage(message);
    });
  }, [messages]);

  return (
    <div className="bg-blue-50 rounded-lg shadow-lg p-3 flex h-full w-full flex-col">
      <div className="flex-1 overflow-y-auto mb-4">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
            deleteMessage={deleteMessage}
          />
        ))}
      </div>
    </div>
  );
};

const ChatMessage = ({
  message,
  deleteMessage,
}: {
  message: MessageType;
  deleteMessage: (id: number) => void;
}) => {
  return (
    <div key={message.id} className="relative">
      <button
        onClick={() => deleteMessage(message.id)}
        className="absolute top-0 right-0 m-2 p-1 text-grey-700 hover:text-red-700"
      >
        <RxCross1 />
      </button>
      <div className="p-4 mb-4 bg-white rounded-lg shadow-md">
        <p style={{ overflowWrap: "anywhere" }}>{message.text}</p>
      </div>
    </div>
  );
};

export default ChatBox;
