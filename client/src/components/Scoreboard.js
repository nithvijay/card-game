const Scoreboard = ({
  scores,
  userNames,
  lastRoundDesc,
  totalNumberOfRounds,
}) => {
  return (
    <div className="p-3">
      <div className="row p-1">
        {scores.map((score, index) => (
          <div className="col" key={index}>
            <div className="card text-center">
              <div className="scorecard-player-name">{userNames[index]}</div>
              <div className="scorecard-player-score">{score}</div>
            </div>
          </div>
        ))}
      </div>
      <div className="row p-1">
        <div className="col">
          <div className="card p-3">Round Number: {totalNumberOfRounds}</div>
        </div>
        <div className="col">
          <div className="card p-3">{lastRoundDesc}</div>
        </div>
      </div>
    </div>
  );
};

export default Scoreboard;
