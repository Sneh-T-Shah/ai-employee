# AI Developer Role: Data Analysis and Reporting System

## Overview

This project involves the development of an AI-driven data analysis and reporting system. It is designed to handle various file formats, perform data analysis, generate comprehensive reports, and interact with users through a web-based UI. Despite the challenges faced, including the limitations of free LLM services, significant progress has been achieved, demonstrating the system's capabilities and future potential.

## Achievements and Challenges

### Accomplishments

1. **Data Processing**:
   - **Data Ingestion**: Successfully implemented functionality to handle data in CSV, JSON, and Excel formats, converting and saving it as CSV to ensure consistency and data integrity.
   - **Preprocessing**: Established a pipeline to manage raw data without unnecessary cleaning, preserving data for accurate analysis.

2. **Analysis Engine**:
   - **Dynamic Analysis**: Created an AI agent capable of dynamically selecting and executing appropriate data analysis techniques based on data characteristics.
   - **Algorithm Implementation**: Incorporated custom agent tools to run the llm generated code to dynamically get the output

3. **Report Generation**:
   - **Comprehensive Reporting**: Utilized the `sweetviz` library for data profiling, generating detailed reports with visualizations and written summaries.

4. **User Interaction**:
   - **Web UI Development**: Developed two Streamlit UIs:
     - **Analysis and Reporting**: For data analysis and report generation.
     - **Chatbot-like Feature**: An interactive interface for user queries, though partially functional due to limitations with free LLM APIs.

5. **Documentation and Testing**:
   - **Documentation**: Provided thorough documentation for code and system architecture.
   - **Testing**: Implemented unit tests to ensure the reliability of critical components.

### Challenges Faced

- **Limited LLM Functionality**: Using free LLM services posed significant challenges with obtaining high-quality responses and executing dynamically generated code, impacting the full functionality of the chatbot-like feature.
- **Time Constraints**: Due to time limitations, the current implementation focuses on core functionalities, highlighting the need for further development.

### Future Potential

- **Enhanced Functionality with Paid LLM Services**: Upgrading to paid LLM services would greatly improve response quality and functionality, enabling more sophisticated interactions and code execution.
- **Extended Capabilities**: With the same agentic approach, future enhancements could include:
  - **Advanced Graphing**: Generating a wider range of visualizations and interactive graphs.
  - **Automated Machine Learning (AutoML)**: Incorporating AutoML to automate model selection and hyperparameter tuning.

## Requirements

To run the project, you need the following libraries:

- `sweetviz` - For data profiling and generating reports.
- `crewai` - For creating and managing AI agents.
- `crewai-tools` - Additional tools for working with CrewAI.
- `langchain_groq` - For managing conversational interactions and generating responses.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Install Dependencies**:
   Create a `requirements.txt` file with the following content:
   ```
   sweetviz
   crewai
   crewai-tools
   langchain_groq
   streamlit
   ```
   Then install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   - For the Streamlit UIs:
     ```bash
     streamlit run ui.py
     streamlit run chat_ui.py
     ```

## Usage

1. **Data Processing**:
   - Load and preprocess data using the Streamlit UI for analysis and reporting.

2. **Analysis**:
   - Perform data analysis through the Streamlit UI.

3. **Report Generation**:
   - Generate and view comprehensive reports via the Streamlit UI.

4. **User Interaction**:
   - Use the chatbot-like feature (in development) for interactive data analysis queries through the Streamlit UI.

## Contribution

Contributions are welcome! Feel free to submit issues or pull requests. Your feedback and enhancements are highly appreciated.