import { SocketContext, socket } from "./context/socket";
import Main from "./components/Main";

const App = () => {
  return (
    <div className="container">
      <SocketContext.Provider value={socket}>
        <Main />
      </SocketContext.Provider>
    </div>
  );
};

export default App;
