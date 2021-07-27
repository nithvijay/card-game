describe("The Home Page", () => {
  it("successfully loads", () => {
    const name = "testUser1";
    const room = "testRoom1";
    cy.visit("/"); // change URL to match your dev URL

    cy.get("input").first().type(name);
    cy.get("input").last().type(room).should("have.value", room.toUpperCase());
    cy.get("button").first().click();
    cy.contains(name);
    cy.task("checkpoint", "first user has joined");

    cy.task("waitForCheckpoint", "second user has joined");
  });
});
