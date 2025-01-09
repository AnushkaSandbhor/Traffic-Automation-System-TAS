const request = require("supertest");
const express = require("express");
const axios = require("axios");
const signinRouter = require("../Controller/UserController"); // Adjusted path

jest.mock("axios"); // Mock axios

const app = express();
app.use(express.json());
app.use("/api", signinRouter);

describe("/signin API Tests", () => {
  it("should return 400 if email or password is missing", async () => {
    const response = await request(app)
      .post("/api/signin")
      .send({ email_id: "" }); // Missing password
    expect(response.status).toBe(400);
    expect(response.body.message).toBe("Email and password are required.");
  });

  it("should return 201 on successful signin", async () => {
    axios.post.mockResolvedValue({
      data: { message: "success", credentials: { token: "testToken" } },
      status: 200,
    });

    const response = await request(app)
      .post("/api/signin")
      .send({ email_id: "test@example.com", password: "password123" });

    expect(response.status).toBe(201);
    expect(response.body.message).toBe("Signin successful");
    expect(response.body.credentials.token).toBe("testToken");
  });

  it("should return Flask error response for failed signin", async () => {
    axios.post.mockRejectedValue({
      response: {
        status: 401,
        data: { message: "Invalid credentials" },
      },
    });

    const response = await request(app)
      .post("/api/signin")
      .send({ email_id: "test@example.com", password: "wrongPassword" });

    expect(response.status).toBe(401);
    expect(response.body.message).toBe("Invalid credentials");
  });

  it("should return 500 for network or server errors", async () => {
    axios.post.mockRejectedValue(new Error("Network Error"));

    const response = await request(app)
      .post("/api/signin")
      .send({ email_id: "test@example.com", password: "password123" });

    expect(response.status).toBe(500);
    expect(response.body.message).toBe("Internal Server Error");
  });
});
