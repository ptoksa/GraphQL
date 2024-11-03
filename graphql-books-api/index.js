const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');

// Define a GraphQL schema
const schema = buildSchema(`
  type Query {
    books: [Book]
  }

  type Book {
    title: String
    author: String
  }
`);

// Sample data
const books = [
  { title: "The Hobbit", author: "J.R.R. Tolkien" },
  { title: "Harry Potter and the Philosopher's Stone", author: "J.K. Rowling" }
];

// Define root resolver
const root = {
  books: () => books,
};

// Set up Express app and GraphQL endpoint
const app = express();
app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true, // Enable GraphiQL UI for testing queries
}));

// Start the server
app.listen(4000, () => {
  console.log('Running a GraphQL API server at http://localhost:4000/graphql');
});
