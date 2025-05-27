import { Container } from "react-bootstrap";
import "../styles/scss/ChatBubble.scss";

interface ChatBubbleProps {
  text: string;
  position: "left" | "right";
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ text, position }) => {
  return (
    <Container className={`message-bubble ${position}`}>
      <div className="bubble-text">{text}</div>
    </Container>
  );
};

export default ChatBubble;