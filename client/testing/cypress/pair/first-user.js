describe("The Home Page", () => {
  it("successfully loads", () => {
    const name = "testUser1";
    const room = "testRoom1";
    const seed = "testingSeed001";
    cy.visit("/"); // change URL to match your dev URL

    cy.get("input").first().type(name);
    cy.get("input").last().type(room).should("have.value", room.toUpperCase());
    cy.get("button").first().click();
    cy.contains(name);

    cy.task("checkpoint", "first user has joined");
    cy.task("waitForCheckpoint", "third user has joined");

    cy.get(":nth-child(2) > :nth-child(3) > label > .cursor-pointer")
      .click()
      .should("contain", "70");
    cy.get(":nth-child(5) > label > .cursor-pointer")
      .click()
      .should("contain", "11");

    cy.get(".bg-gray-100")
      .click()
      .type(seed, { delay: 70 })
      .should("have.value", seed);

    cy.task("checkpoint", "done changing settings");

    cy.task("waitForCheckpoint", "third user ready up");
    cy.task("waitForCheckpoint", "second user ready up");

    cy.reload();
    cy.get("input").first().should("have.value", name);
    cy.get("input").last().should("have.value", room.toUpperCase());
    cy.get("button").first().click();

    cy.get(":nth-child(2) > :nth-child(3) > label > .cursor-pointer").should(
      "contain",
      "70"
    );
    cy.get(":nth-child(5) > label > .cursor-pointer").should("contain", "11");
    cy.get(".bg-gray-100").should("have.value", seed);
    cy.task("checkpoint", "first user ready up");
    // cy.get(".text-lg").click();
  });
});
