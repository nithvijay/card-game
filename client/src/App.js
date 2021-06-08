import { SocketContext, socket } from "./context/socket";
import Main from "./components/Main";

const App = () => {
  return (
    <div className="app">
      <SocketContext.Provider value={socket}>
        <Main />
      </SocketContext.Provider>
    </div>
  );
};

export default App;
