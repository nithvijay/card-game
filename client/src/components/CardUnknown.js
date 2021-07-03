const CardUnknown = ({ id }) => {
    return (
      <div className="p-1">
        <div
          className="card d-flex justify-content-center align-items-center"
          style={{ width: "8rem", height: "12rem" }}
        >
            <div>Enemy's Card</div>
          <div>ID: {id}</div>
        </div>
      </div>
    );
  };
  
  export default CardUnknown;
  