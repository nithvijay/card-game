const EnergyBar = ({ level, maxLevel }) => {
  const arr = [];
  for (let i = 0; i < parseInt(level); i++) {
    arr.push(true);
  }
  for (let i = 0; i < parseInt(maxLevel) - parseInt(level); i++) {
    arr.push(false);
  }

  return (
    <div className="d-flex justify-content-center m-1">
      {arr.map((ele, index) => (
        <div key={index} className={"energy-cell m-1 " + (ele ? "active" : "inactive")}></div>
      ))}
    </div>
  );
};

export default EnergyBar;
