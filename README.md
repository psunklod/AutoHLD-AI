# AutoHLD AI

### AI-Assisted AUTOSAR High-Level Design Analysis

AutoHLD AI is an AI-powered engineering assistant designed to analyze AUTOSAR High-Level Design (HLD) documents and support architecture review workflows.

The system combines **Retrieval-Augmented Generation (RAG)**, **local AI models**, **deterministic architecture extraction**, **HLD revision comparison**, and **engineering impact analysis** in a single interactive interface.

> **Candidate Prototype — Engineering Review Required**

---

## 🚗 Project Overview

Automotive software architectures are often documented in large High-Level Design documents containing software components, interfaces, ports, signals, and dependencies.

Reviewing these documents manually can be time-consuming, especially when engineers need to:

- Find specific architecture information
- Understand dependencies between components
- Compare different HLD revisions
- Identify changes and their potential impact
- Verify information against the original document

**AutoHLD AI** provides an AI-assisted workflow for these tasks while keeping responses grounded in the provided HLD documents.

---

## ✨ Key Features

### 1. 📄 HLD Document Ingestion

Upload AUTOSAR HLD PDF documents and extract their content page-by-page while preserving:

- Page information
- Section information
- Engineering terminology
- Document structure

---

### 2. 🧩 AUTOSAR Architecture Extraction

Automatically identify important architecture entities such as:

- Software Components
- Interfaces
- Ports
- Signals
- Dependencies

The prototype combines deterministic extraction rules with AI-assisted analysis.

---

### 3. 🔎 Grounded HLD Question Answering

Ask engineering questions about the uploaded HLD.

Example:

> What are the dependencies between the software components?

The system retrieves the most relevant HLD sections and provides an answer based on the retrieved context.

Each answer includes source information such as:

```text
Page 1 | Section 2. Software Components
Page 2 | Section 6. Dependencies
Page 3 | Section 9. Review Notes

**AutoHLD AI - AI-Assisted AUTOSAR HLD Engineering Analysis**

> Candidate Prototype - Engineering Review Required