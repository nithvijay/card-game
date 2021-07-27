describe("The Home Page", () => {
  it("successfully loads", () => {
    const name = "testUser2";
    const room = "testRoom1";

    cy.task("waitForCheckpoint", "first user has joined");

    cy.visit("/"); // change URL to match your dev URL
    cy.get("input").first().type(name);
    cy.get("input").last().type(room).should("have.value", room.toUpperCase());
    cy.get("button").first().click();
    cy.contains(name);

    cy.task("checkpoint", "second user has joined");
  });
});
