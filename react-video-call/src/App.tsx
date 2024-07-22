import ChatBox from "./components/ChatBox";
import VideoCall from "./components/VideoCall";
import Transcript from "./components/Transcript";
import Emotion from "./components/Emotion";

const App = () => {
  return (
    <div className="h-screen bg-black flex flex-col justify-center items-center">
      <div className="grid grid-cols-4 w-full h-full">
        <div className="relative col-span-3 bg-blue-100 justify-center items-center">
          <VideoCall />
          <Transcript />
          <Emotion />
        </div>
        <div className="col-span-1 bg-white p-2 flex flex-col items-center shadow-lg h-screen">
          <h1 className="text-3xl font-bold mb-2 border-b-2">
            Bot Insights 🔮
          </h1>
          <ChatBox />
        </div>
      </div>
    </div>
  );
};

export default App;
