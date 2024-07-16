import {
  CallingState,
  StreamCall,
  StreamVideo,
  StreamVideoClient,
  useCallStateHooks,
  User,
  StreamTheme,
  StreamVideoParticipant,
  ParticipantView,
} from "@stream-io/video-react-sdk";

import "@stream-io/video-react-sdk/dist/css/styles.css";
import { useEffect } from "react";
import resampleTo16kHZ from "../utils/audio";
import { socket } from "../socket";

// Remember to update the API key and token values because it changes every day.
const apiKey = "ta4p357cjet3";
const token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTWFydGluIn0.6gc-lipzOpk6DXK1SKC_xlQymDY5ogk36KPi0OdCPwU";
const userId = "Martin";
const callId = "Martin-Testing-Room";

// set up the user object
const user: User = {
  id: userId,
  image: "https://getstream.io/random_svg/?id=oliver&name=Oliver",
};

const client = new StreamVideoClient({ apiKey, user, token });
const call = client.call("default", callId);
await call.join({ create: true });

const VideoCall = () => {
  useEffect(() => {
    const getMediaStream = async () => {
      const audioDataCache = [];
      const context = new AudioContext();
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      const mediaStream = context.createMediaStreamSource(stream);
      const recorder = context.createScriptProcessor(4096, 1, 1);

      recorder.onaudioprocess = async (event) => {
        const inputData = event.inputBuffer.getChannelData(0);
        const audioData16kHz = resampleTo16kHZ(inputData, context.sampleRate);

        audioDataCache.push(inputData);

        socket.emit("audio", audioData16kHz);
      };

      // Prevent page mute
      mediaStream.connect(recorder);
      recorder.connect(context.destination);
      mediaStream.connect(context.destination);
    };

    getMediaStream();
  }, []);

  return (
    <StreamVideo client={client}>
      <StreamCall call={call}>
        <StreamLayout />
      </StreamCall>
    </StreamVideo>
  );
};

export const ParticipantList = (props: {
  participants: StreamVideoParticipant[];
}) => {
  const { participants } = props;
  return (
    <div className="flex flex-row h-full w-full gap-2">
      {participants.map((participant) => {
        return (
          <ParticipantView
            participant={participant}
            key={participant.sessionId}
          />
        );
      })}
    </div>
  );
};

const FloatingLocalParticipant = (props: {
  participant?: StreamVideoParticipant;
}) => {
  const { participant } = props;
  return (
    <div
      style={{
        position: "absolute",
        top: "15px",
        left: "15px",
        width: "240px",
        height: "135px",
        boxShadow: "rgba(0,0,0, 0.1) 0px 0px 10px 3px",
        borderRadius: "12px",
      }}
    >
      <ParticipantView participant={participant!} />
    </div>
  );
};

const StreamLayout = () => {
  const { useCallCallingState, useLocalParticipant, useRemoteParticipants } =
    useCallStateHooks();

  const callingState = useCallCallingState();
  const localParticipant = useLocalParticipant();
  const remoteParticipants = useRemoteParticipants();

  if (callingState !== CallingState.JOINED) {
    return <div>Loading...</div>;
  }

  return (
    <StreamTheme>
      <ParticipantList participants={remoteParticipants} />
      <FloatingLocalParticipant participant={localParticipant} />
    </StreamTheme>
  );
};

export default VideoCall;
