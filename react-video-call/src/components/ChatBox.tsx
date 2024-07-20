import { useEffect, useState } from "react";
import {
  IoClose,
  IoThumbsUpOutline,
  IoThumbsDownOutline,
} from "react-icons/io5";
import { socket } from "../socket";
import { AnimatePresence, motion } from "framer-motion";

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

    socket.on("rag", (data) => {
      const message: MessageType = {
        id: Math.random(),
        text: data,
      };
      addMessage(message);
    });
  }, [messages]);

  return (
    <div className="bg-blue-50 rounded-lg shadow-lg p-3 flex h-full w-full flex-col h-full overflow-y-auto">
      <motion.ul
        layout
        layoutId={"list"}
        className="flex-1 flex flex-col-reverse justify-end mb-4"
      >
        <AnimatePresence>
          {messages.map((message) => (
            <motion.li
              initial={{ x: -50, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: -50, opacity: 0 }}
              key={message.id}
              layout
            >
              <ChatMessage message={message} deleteMessage={deleteMessage} />
            </motion.li>
          ))}
        </AnimatePresence>
      </motion.ul>
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
    <div className="mb-4 bg-white rounded-lg shadow-md" key={message.id}>
      <div className="flex justify-end p-1 pb-0">
        <button
          onClick={() => deleteMessage(message.id)}
          className="p-1 text-grey-700 hover:text-red-700 hover:bg-gray-200 rounded"
        >
          <IoClose size={25} />
        </button>
      </div>
      <div className="px-4 pb-3">
        <p style={{ overflowWrap: "anywhere" }}>{message.text}</p>
        <div className="flex space-x-2 mt-2">
          <button className="p-1 text-green-700 hover:text-green-700 hover:bg-gray-200 rounded">
            <IoThumbsUpOutline size={20} />
          </button>
          <button className="p-1 text-red-700 hover:text-red-700 hover:bg-gray-200 rounded">
            <IoThumbsDownOutline size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
