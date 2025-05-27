import React from "react";
import MessageCard from "./MessageCard";
import "../styles/scss/SequenceStep.scss";


interface SequenceStepProps {
  title: string;
  sequence_id: string;
  step: number;
  linkedinMessage: string;
  emailMessage: string;
}

const SequenceStep: React.FC<SequenceStepProps> = ({
  title,
  sequence_id,
  step,
  linkedinMessage,
  emailMessage,
}) => {
  return (
    <div className="sequence-step">
      <div className="step-header">
        <h6>{title}</h6>
      </div>
      {/* <MessageCard type="linkedin" message={linkedinMessage} step={step} sequence_id={sequence_id}/>
      <MessageCard type="email" message={emailMessage} step={step} sequence_id={sequence_id}/> */}
      {linkedinMessage.trim() && (
        <MessageCard
          type="linkedin"
          message={linkedinMessage}
          step={step}
          sequence_id={sequence_id}
        />
      )}
      {emailMessage.trim() && (
        <MessageCard
          type="email"
          message={emailMessage}
          step={step}
          sequence_id={sequence_id}
        />
      )}
    </div>
  );
};

export default SequenceStep;