<template>
  <div>
    <h2>News Articles</h2>
    <ul>
      <li v-for="article in articles" :key="article.id">
        <h3>{{ article.title }}</h3>
        <p>{{ article.content }}</p>
        <p>Category: {{ article.category.name }}</p>
        <p>Published on: {{ article.publication_date }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      articles: [],
    };
  },
  mounted() {
    this.fetchNews();
  },
  methods: {
    fetchNews() {
      axios
        .get("http://127.0.0.1:8000/api/news") // Update with the actual endpoint
        .then((response) => {
          this.articles = response.data.articles;
        })
        .catch((error) => {
          console.log("Error fetching news:", error);
        });
    },
  },
};
</script>
