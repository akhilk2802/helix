import { useState, useEffect } from "react";
import "../styles/scss/chat.scss";
import ChatBubble from "./ChatBubble";
import { Container, Button } from "react-bootstrap";
import socket from "../socket";

interface ChatProps {
  setSequence: (seq: any[]) => void;
}

const Chat: React.FC<ChatProps> = ({ setSequence }) => {

    type Message = {
        sender: "user" | "helix";
        text: string;
    };  
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState<Message[]>([]);
    const [isThinking, setIsThinking] = useState(false);
    const [intentMessage, setIntentMessage] = useState<string | null>(null);
    const [userInfo, setUserInfo] = useState<{ id: string; name: string; company: string } | null>(null);

    useEffect(() => {
        const userData = localStorage.getItem("user");
        if (userData) {
            const parsed = JSON.parse(userData);
            setUserInfo({ id: parsed.id, name: parsed.name, company: parsed.company });

            setMessages([
                {
                    sender: "helix",
                    text: `Hi ${parsed.name}, how can I assist you today?`
                }
                ]);
        }
    }, []);

    const sendMessage = () => {

        if (!input.trim() || !userInfo) return;
        setMessages((prev) => [...prev, { sender: "user", text: input }]);
        setIsThinking(true);

        if (!input.trim()|| !userInfo) return;
        
        const user_sessionId = localStorage.getItem("user_sessionId");
        // console.log("sessaionid -> ", sessionId)
        

        socket.emit("send_message", {
            user_id: userInfo.id,
            session_id: user_sessionId,
            message: input,
            rec_name: userInfo.name,
            company: userInfo.company,
        });
        setInput("");
    };

    useEffect(() => {
        socket.on("receive_message", (data) => {
            console.log("data r-> ", data)
            setMessages((prev) => [...prev, { sender: "helix", text: data.response.agent }]);

            console.log("sequence -> ", data.response.sequence)
            if (data.response.sequence) { 
                // setSequence(data.response.sequence); 
                setSequence([...data.response.sequence]);            }
            setIsThinking(false);
            setIntentMessage(null);
        });

        socket.on("chat_error", (error) => {
            console.error("Socket error:", error);
            setIsThinking(false);
            setIntentMessage(null);
        });

        return () => {
            socket.off("receive_message");
            socket.off("chat_error");
        };
    }, []);

    useEffect(() => {
        socket.on("tool_call", (data) => {
            console.log("Tool detected early:", data.tool);
            const toolMessageMap: { [key: string]: string } = {
            create_sequence: "🛠 Generating a recruiting sequence...",
            edit_sequence: "✏️ Editing the sequence...",
            delete_step: "🗑 Deleting a step...",
            };

            setIsThinking(true);
            setIntentMessage(toolMessageMap[data.tool] || "Helix is Thinking...");
        });

        return () => {
            socket.off("tool_call");
        };
        }, []);

    return (
        <Container className="chat-window">
            <div className="chat-convo">
                {messages.map((msg, idx) => (
                    <ChatBubble
                        key={idx}
                        text={msg.text}
                        position={msg.sender === "user" ? "right" : "left"}
                    />
                ))}
                {isThinking && intentMessage && (
                    <ChatBubble
                        text={intentMessage}
                        position="left"
                    />
                )}
            </div>
            <div className="chat-input">
                <input
                    type="text"
                    placeholder="Type your message..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                    className="form-control"
                />
                <Button onClick={sendMessage}>Send</Button>
            </div>
        </Container>
    );
};
export default Chat;
