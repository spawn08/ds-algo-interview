# Datastructures and Algorithms Interview Questions

![GitHub contributors](https://img.shields.io/github/contributors/spawn08/ds-algo-interview)
![GitHub stars](https://img.shields.io/github/stars/spawn08/ds-algo-interview?style=social)
![GitHub forks](https://img.shields.io/github/forks/spawn08/ds-algo-interview?style=social)
![GitHub issues](https://img.shields.io/github/issues/spawn08/ds-algo-interview)

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/f/f8/Python_logo_and_wordmark.svg" alt="Python" width="100"/>
  <img src="https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Java_programming_language_logo.svg/121px-Java_programming_language_logo.svg.png" alt="Java" width="50"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Go_Logo_Blue.svg/512px-Go_Logo_Blue.svg.png" alt="Golang" width="80"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/JavaScript-logo.png/600px-JavaScript-logo.png" alt="JavaScript" width="50"/>
</p>

## 🎮 Interactive Learning Site

**▶ Live site: https://spawn08.github.io/ds-algo-interview/**

This repo ships with an interactive documentation website (in [`docs/`](docs/)) built for
people preparing for MAANG/FAANG interviews. For each problem you get:

- 📖 The problem, the **intuition**, and — importantly — **why** a particular data structure or
  technique was chosen (the part interviewers actually probe).
- ▶️ A **step-by-step visualization** you can play, pause, and scrub — watch pointers move, the
  hash map fill, the stack push/pop, the DP grid populate, and BFS/DFS sweep a tree or graph.
- ⏱️ Time & space **complexity** with notes.
- ⌨️ The **real Java & Python code** from this repo (generated straight from the source files, so
  it never drifts), with copy-to-clipboard and **live in-browser Python execution** (via Pyodide).

The site is a dependency-free static SPA — just HTML/CSS/JS — and deploys automatically to GitHub
Pages via [GitHub Actions](.github/workflows/deploy-pages.yml).

## 📋 Table of Contents
- [Interactive Learning Site](#-interactive-learning-site)
- [Overview](#overview)
- [Languages](#languages)
- [Problem Categories](#problem-categories)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
- [Running the Site Locally](#-running-the-site-locally)
- [Running the Tests](#-running-the-tests)
- [How to Contribute](#how-to-contribute)
- [Learning Resources](#learning-resources)
- [License](#license)

## 🌟 Overview

This repository contains comprehensive code examples for data structures, algorithms, LeetCode and GeeksforGeeks problems commonly asked in top product company interviews. Solutions are provided in multiple languages including Java, Python, Golang, and JavaScript.

The goal is to create a centralized, well-documented resource that helps developers prepare for technical interviews at leading tech companies.

<p align="center">
  <img src="https://cdn.pixabay.com/photo/2016/11/19/14/00/code-1839406_1280.jpg" alt="Coding" width="600"/>
</p>

## 💻 Languages

Solutions are implemented in the following languages:

| Language | Description |
|----------|-------------|
| ![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white) | Object-oriented solutions with detailed comments |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | Clean, Pythonic implementations with type hints |
| ![Golang](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white) | Efficient Go implementations |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) | Modern JavaScript solutions with ES6+ features |

## 🧩 Problem Categories

| Category | Description | Count |
|----------|-------------|-------|
| **Data Structures** | Arrays, Linked Lists, Trees, Graphs, Hash Tables, Stacks, Queues, Heaps | 50+ |
| **Algorithms** | Sorting, Searching, Dynamic Programming, Greedy, Divide & Conquer | 40+ |
| **LeetCode** | Solutions to popular LeetCode problems with difficulty tags | 100+ |
| **GeeksforGeeks** | Solutions to important GeeksforGeeks problems | 75+ |

## 📁 Directory Structure

```
.
├── data-structures/
│   ├── arrays/
│   ├── linked-lists/
│   ├── trees/
│   ├── graphs/
│   ├── hash-tables/
│   └── ...
├── algorithms/
│   ├── sorting/
│   ├── searching/
│   ├── dynamic-programming/
│   └── ...
├── leetcode/
│   ├── easy/
│   ├── medium/
│   └── hard/
├── geeksforgeeks/
└── language-specific/
    ├── java/
    ├── python/
    ├── golang/
    └── javascript/
```

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/spawn08/ds-algo-interview.git
   cd ds-algo-interview-java
   ```

2. Navigate to the problem category you're interested in:
   ```bash
   cd data-structures/arrays
   ```

3. Each problem includes:
   - Problem statement
   - Multiple language implementations
   - Time and space complexity analysis
   - Test cases

## 🖥️ Running the Site Locally

The site is fully static, so any HTTP server works:

```bash
cd docs
python3 -m http.server 8000
# open http://localhost:8000
```

The content shown on the site is generated from the actual source files plus a curated catalog of
explanations in [`scripts/generate_site.py`](scripts/generate_site.py). After editing a solution
file (or adding a new problem to the catalog), regenerate the data file:

```bash
python3 scripts/generate_site.py   # rewrites docs/data/problems.js
```

A CI check fails the build if `docs/data/problems.js` is out of date, so the displayed code always
matches the repo.

## ✅ Running the Tests

**Python** (uses `pytest`):

```bash
cd python
python3 -m pytest tests/ -q
```

**Java** (no build tool required — a tiny dependency-free harness):

```bash
cd java
javac -d bin-test $(find src test -name '*.java')
java -cp bin-test com.dsalgo.RunAllTests
```

Both suites also run automatically on every push via
[GitHub Actions](.github/workflows/tests.yml).

## 🤝 How to Contribute

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code:
- Includes detailed comments
- Has proper time and space complexity analysis
- Passes all existing tests
- Follows the project coding style

## 📚 Learning Resources

<p align="center">
  <img src="https://cdn.pixabay.com/photo/2015/07/17/22/43/student-849825_1280.jpg" alt="Learning" width="400"/>
</p>

- [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
- [LeetCode](https://leetcode.com/)
- [GeeksforGeeks](https://www.geeksforgeeks.org/)
- [Hackerrank](https://www.hackerrank.com/)
- [Cracking the Coding Interview](http://www.crackingthecodinginterview.com/)

## 📄 License

This repository is available under the MIT License. See the [LICENSE](LICENSE) file for more info.

---

<p align="center">
  <i>If you found this repository helpful, please consider giving it a ⭐!</i>
</p>
