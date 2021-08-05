describe("The Home Page", () => {
  it("successfully loads", () => {
    const name = "testUser2";
    const room = "testRoom1";
    const seed = "testingSeed001";

    cy.task("waitForCheckpoint", "first user has joined");

    cy.visit("/"); // change URL to match your dev URL
    cy.get("input").first().type(name);
    cy.get("input").last().type(room).should("have.value", room.toUpperCase());
    cy.get("button").first().click();
    cy.contains(name);

    cy.task("checkpoint", "second user has joined");

    cy.task("waitForCheckpoint", "third user has joined");
    cy.task("waitForCheckpoint", "done changing settings");

    cy.get(":nth-child(2) > :nth-child(3) > label > .cursor-pointer").should("contain", "70");
    cy.get(":nth-child(5) > label > .cursor-pointer").should("contain", "11");
    cy.get(".bg-gray-100").should("have.value", seed);

    cy.task("waitForCheckpoint", "third user ready up");
    cy.get(".text-lg").click();
    cy.task("checkpoint", "second user ready up");
    cy.task("waitForCheckpoint", "first user ready up");
  });
});
