import "../styles/scss/Home.scss"
import {useState} from "react"
import Chat from "./Chat"
import Header from "./Header"
import Workspace from "./Workspace"
import { Container } from "react-bootstrap"
import {
  PanelGroup,
  Panel,
  PanelResizeHandle,
} from "react-resizable-panels"


const Home: React.FC = () => {
    const [sequence, setSequence] = useState<any[]>([]);
    // const [sequences, setSequences] = useState<any[][]>([]);

    return (
        <>
        
        <Container fluid className="home-main">
            <Header/>
            <PanelGroup direction="horizontal">
                <Panel defaultSize={40}>
                    <div className="panel-content">
                        <div className="helix-header">
                            <span className="helix-title">Chat with AI</span>
                        </div>
                        <Container className="chat-panel">
                            <Chat setSequence={setSequence}/>
                            
                            {/* <Chat setSequence={(newSeq) => setSequences((prev) => [...prev, newSeq])} /> */}
                        </Container>
                    </div>
                </Panel>
                <PanelResizeHandle className="resize-handle" />
                <Panel>
                    <div className="panel-content">
                        <div className="workspace-header">
                            <span className="workspace-title">Workspace</span>
                        </div>
                        <Container className="workspace-panel">
                            <Workspace sequence={sequence}/>
                            {/* <Workspace sequences={sequences} /> */}
                        </Container>
                    </div>
                </Panel>
            </PanelGroup>
        </Container>
        </>
    );
}
export default Home;