import React, { useState, useEffect } from "react";
import SequenceStep from "./SequenceStep";
import "../styles/scss/Workspace.scss";


interface WorkspaceProps {
  sequence: { step: number; channel: string; content: string; sequence_id: string }[];
}

const Workspace: React.FC<WorkspaceProps> = ({ sequence }) => {
  // const groupedSteps: any = {};

  // sequence.forEach(({ step, channel, content, sequence_id }) => {
  //   if (!groupedSteps[step]) {
  //     groupedSteps[step] = {
  //       id: step,
  //       title: `Step ${step}`,
  //       sequence_id,
  //       linkedinMessage: "",
  //       emailMessage: ""
  //     };
  //   }
  //   if (channel === "linkedin") groupedSteps[step].linkedinMessage = content;
  //   if (channel === "email") groupedSteps[step].emailMessage = content;
  // });

  // const stepsArray = Object.values(groupedSteps);

  const [stepsArray, setStepsArray] = useState<any[]>([]);

  useEffect(() => {
    const groupedSteps: any = {};

    sequence.forEach(({ step, channel, content, sequence_id }) => {
      if (!groupedSteps[step]) {
        groupedSteps[step] = {
          id: step,
          title: `Step ${step}`,
          sequence_id,
          linkedinMessage: "",
          emailMessage: "",
        };
      }
      if (channel === "linkedin") groupedSteps[step].linkedinMessage = content;
      if (channel === "email") groupedSteps[step].emailMessage = content;
    });

    setStepsArray(Object.values(groupedSteps));
  }, [sequence]);

  return (
    <div className="workspace">
      {stepsArray.map((step: any) => (
        <SequenceStep
          key={`${step.sequence_id}-${step.id}-${step.linkedinMessage}-${step.emailMessage}`}
          title={step.title}
          sequence_id={step.sequence_id}
          step={step.id}
          linkedinMessage={step.linkedinMessage}
          emailMessage={step.emailMessage}
        />
      ))}
    </div>
  );
};


export default Workspace;