const CardUnknown = ({ id }) => {
    return (
      <div className="p-1">
        <div
          className="card"
          style={{ width: "8rem", height: "16rem" }}
        >
            <div>Unknown</div>
          <div>ID: {id}</div>
        </div>
      </div>
    );
  };
  
  export default CardUnknown;
  