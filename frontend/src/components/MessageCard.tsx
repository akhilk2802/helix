import React, { useState, useRef, useEffect } from "react";
import { Card, Form } from "react-bootstrap";
import "../styles/scss/MessageCard.scss";
import { SocialIcon } from 'react-social-icons'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from '@fortawesome/free-solid-svg-icons'
import { toast } from "react-toastify";


interface MessageCardProps {
  type: "linkedin" | "email";
  message: string;
  step: number;
  sequence_id: string;
}

const MessageCard: React.FC<MessageCardProps> = ({ type, message, step, sequence_id }) => {
  const [draft, setDraft] = useState(message);
  const [timer, setTimer] = useState<NodeJS.Timeout | null>(null);
  const [deleted, setDeleted] = useState(false);

  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"; // Reset height
      textareaRef.current.style.height = textareaRef.current.scrollHeight + "px"; // Set to scrollHeight
    }
  }, [draft]);

  if (deleted) return null;

  const handleDelete = async () => {
    try {
      // console.log("data to delete -> ", sequence_id, step, type)
      const res = await fetch(`${process.env.REACT_APP_API_URL}:${process.env.REACT_APP_PORT}/api/sequence/delete`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sequence_id,
          step,
          channel: type,
        }),
      });

      if (!res.ok) throw new Error("Failed to delete");

      setDeleted(true); // hide from UI
      toast.success(`Deleted step ${step} on ${type}`);
      // console.log(`Deleted step ${step} on ${type}`);
    } catch (err) {
      toast.error("Delete failed");
      // console.error("Delete failed:", err);
    }
  };


  const saveEdit = async () => {
    try {

      console.log("Sending edit payload:", {
        sequence_id,
        step,
        channel: type,
        new_content: draft,
      });

      const res = await fetch(`${process.env.REACT_APP_API_URL}:${process.env.REACT_APP_PORT}/api/sequence/edit`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sequence_id,
          step,
          channel: type,
          new_content: draft,
        }),
      });
      if (!res.ok) throw new Error("Edit failed");

      toast.success(`Auto-saved step ${step} on ${type}`);
    } catch (err) {
      toast.error("Autosave failed");
      console.error("Autosave failed:", err);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    console.log("changed -> ", e.target.value)
    setDraft(e.target.value);
    if (timer) clearTimeout(timer);
    setTimer(setTimeout(saveEdit, 2000)); // debounce save after 2s
  };

  return (
    <Card className="message-card">
      <Card.Body>
        <div className="card-header">
          <SocialIcon
            network={type}
            style={{ height: 30, width: 30 }}
            bgColor="transparent"
            fgColor={type === "linkedin" ? "#0a66c2" : "#d44638"}
          />
          <div className="delete-icon" onClick={handleDelete}>
            <FontAwesomeIcon icon={faTrash} />
          </div>
        </div>

        <Form.Control
          as="textarea"
          ref={textareaRef}
          rows={1} // Only one row, will grow dynamically
          className="message-box"
          value={draft}
          onChange={handleChange}
          style={{ overflow: "hidden", resize: "none" }} // Prevent scrollbar + manual resizing
        />
      </Card.Body>
    </Card>
  );
};

export default MessageCard;