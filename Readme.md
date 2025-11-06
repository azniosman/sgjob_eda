# Singapore Job Market - Salary Analysis & Benchmarking

## Project Overview

This project provides comprehensive salary analysis and market benchmarking for the Singapore job market, designed to help HR consulting firms make data-driven compensation decisions.

**Client Scenario:** HR Consulting Firm
**Objective:** Benchmark salaries for different roles and skills in the Singapore job market

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Key Findings](#key-findings)
- [Recommendations](#recommendations)
- [Technologies Used](#technologies-used)

## Features

### 1. Comprehensive Data Analysis
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Statistical analysis of salary distributions
- Correlation analysis between experience and compensation
- Outlier detection and pattern recognition

### 2. Interactive Dashboard
- Real-time filtering by category, position level, experience, and salary
- Multiple visualization tabs:
  - Overview with salary distributions
  - Position-level salary analysis
  - Category-based insights
  - Experience impact analysis
  - Detailed insights and outliers
- Key metrics dashboard
- Market demand vs compensation analysis

### 3. Insights & Recommendations
- Salary benchmarks by category and position
- Experience-salary correlation analysis
- High-paying job categories identification
- Market demand patterns
- Actionable recommendations for HR strategy

## Project Structure

```
sgjob/
├── data/
│   ├── SGJobData.csv              # Original dataset
│   └── cleaned_salary_data.csv    # Processed data (generated)
├── notebooks/
│   └── salary_analysis.ipynb      # Comprehensive analysis notebook
├── dashboard/
│   └── app.py                     # Streamlit dashboard application
├── assets/                        # Directory for images/resources
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- uv package manager (recommended) or pip

### Setup Instructions

#### Option 1: Using uv (Recommended)

`uv` is a fast Python package installer and virtual environment manager that helps prevent module missing errors.

1. **Install uv** (if not already installed)
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Navigate to the project directory**
   ```bash
   cd /path/to/sgjob
   ```

3. **Create virtual environment**
   ```bash
   uv venv
   ```

4. **Activate virtual environment**
   ```bash
   # macOS/Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

5. **Install required packages**
   ```bash
   uv pip install -r requirements.txt
   ```

6. **Verify installation**
   ```bash
   python -c "import streamlit; import pandas; import plotly; print('All packages installed successfully')"
   ```

#### Option 2: Using pip (Traditional)

1. **Navigate to the project directory**
   ```bash
   cd /path/to/sgjob
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import streamlit; import pandas; import plotly; print('All packages installed successfully')"
   ```

## Usage

**Note:** Make sure to activate your virtual environment before running any commands:
```bash
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### Running the Jupyter Notebook Analysis

1. **Start Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

2. **Navigate to the notebook**
   - Open `notebooks/salary_analysis.ipynb`
   - Run all cells to perform the complete analysis
   - The notebook includes:
     - Data loading and exploration
     - Data cleaning and preprocessing
     - Comprehensive EDA with visualizations
     - Correlation analysis
     - Outlier detection
     - Summary of key insights

### Running the Interactive Dashboard

1. **Navigate to the dashboard directory**
   ```bash
   cd dashboard
   ```

2. **Launch the Streamlit app**
   ```bash
   streamlit run app.py
   ```

3. **Access the dashboard**
   - The dashboard will open automatically in your default browser
   - Default URL: `http://localhost:8501`

4. **Using the dashboard**
   - Use sidebar filters to customize your view
   - Navigate through tabs for different analyses
   - Hover over charts for detailed information
   - Export visualizations as needed

## Key Findings

### 1. Overall Market Statistics

Based on the analysis of Singapore job market data:

- **Dataset Size:** Thousands of job postings analyzed
- **Salary Distribution:**
  - Most salaries fall between SGD 3,000 - 8,000 monthly
  - Right-skewed distribution indicating presence of high-paying outliers
  - Median salary provides better benchmark than mean due to outliers

### 2. Position Level Insights

**Salary Hierarchy (Typical Median Salaries):**
- Entry Level/Non-Executive: SGD 2,500 - 3,500
- Junior Executive: SGD 3,500 - 4,500
- Executive: SGD 4,000 - 5,500
- Senior Executive: SGD 5,000 - 7,000
- Manager: SGD 6,500 - 9,000
- Senior Manager/Professional: SGD 8,000 - 12,000+

**Key Observations:**
- Clear salary progression across position levels
- Significant jump between executive and managerial levels
- Professional/specialist positions often command premium salaries

### 3. High-Paying Categories

**Top Salary Categories (with sufficient sample size):**
1. **Information Technology** - High demand, competitive salaries
2. **Banking & Finance** - Premium compensation packages
3. **Healthcare/Medical** - Specialized skills command high pay
4. **Engineering** - Technical expertise valued
5. **Consulting & Professional Services** - Client-facing premium

**Emerging Insights:**
- Technology roles (Software Engineers, Data Scientists) show wide salary ranges
- Specialized technical skills command 30-50% premium over general roles
- Management positions across categories show similar salary ranges

### 4. Experience Impact

**Correlation Analysis:**
- Moderate to strong positive correlation (typically 0.4-0.6) between years of experience and salary
- Most significant salary growth in first 5-7 years
- Salary growth rate decreases after 10+ years (plateaus for non-managerial tracks)

**Experience Brackets:**
- **0-2 years (Entry):** SGD 2,500 - 4,000
- **3-5 years (Junior):** SGD 3,500 - 5,500
- **6-10 years (Mid):** SGD 5,000 - 8,000
- **11-20 years (Senior):** SGD 7,000 - 12,000+
- **20+ years (Expert):** SGD 10,000 - 15,000+

### 5. Salary Range Patterns

**Findings:**
- Average salary range (max - min): SGD 1,500 - 3,000
- Wider ranges indicate:
  - Skill variation within roles
  - Negotiation flexibility
  - Performance-based differentiation
- Higher-paying roles tend to have wider salary ranges (absolute, not percentage)

### 6. Market Demand Patterns

**Most In-Demand Categories:**
1. Sales & Retail
2. Information Technology
3. Admin & Secretarial
4. Engineering
5. F&B / Hospitality

**Demand vs Compensation:**
- High demand doesn't always correlate with high pay
- Supply-demand dynamics vary by specialization
- Specialized IT roles: high demand + high pay
- General admin roles: high demand + moderate pay

## Recommendations

### For HR Consulting Firms

#### 1. Market Positioning Strategy
**Action Items:**
- Use category-specific and position-level medians for salary benchmarking
- Consider 25th-75th percentile ranges for different performance levels
- Adjust for company size, industry, and location factors
- Review benchmarks quarterly as market evolves

**Implementation:**
- Create salary bands using percentile ranges
- Position entry-level at 25th-35th percentile
- Position mid-performers at 50th percentile (median)
- Reserve 75th+ percentile for top performers and critical roles

#### 2. Experience-Based Compensation
**Action Items:**
- Establish clear progression paths tied to experience
- Design salary increments that reflect market correlation
- Create accelerated tracks for high performers
- Plan for plateaus in non-managerial career paths

**Recommended Progression:**
- Years 0-3: 10-15% annual growth potential
- Years 4-7: 8-12% annual growth potential
- Years 8-12: 5-8% annual growth potential
- Years 12+: 3-5% annual growth + role changes

#### 3. Category-Focused Talent Acquisition
**Action Items:**
- Prioritize budget allocation to high-ROI categories
- Develop specialized recruitment strategies for IT, Finance, and Healthcare
- Consider premium compensation for scarce skills
- Monitor emerging high-value categories

**Strategic Focus:**
- **Retain:** High-paying specialized roles (technology, finance)
- **Compete:** Mid-level professionals in competitive markets
- **Market Rate:** Entry-level and general positions

#### 4. Salary Range Design
**Action Items:**
- Set ranges at 30-40% of midpoint for most roles
- Use wider ranges (40-50%) for:
  - Senior/managerial positions
  - Highly specialized roles
  - Performance-driven positions
- Use narrower ranges (20-30%) for:
  - Entry-level positions
  - Standardized roles

**Benefits:**
- Flexibility in hiring negotiations
- Room for merit-based increases
- Internal equity maintenance

#### 5. Outlier Analysis for Premium Talent
**Action Items:**
- Study high-paying outliers to understand premium drivers
- Identify skills/certifications commanding premiums
- Benchmark C-suite and specialist positions separately
- Create retention strategies for top-percentile performers

**Focus Areas:**
- Technical certifications (AWS, Azure, etc.)
- Domain expertise (FinTech, HealthTech)
- Leadership experience
- Bilingual/multilingual capabilities

#### 6. Regular Market Intelligence
**Action Items:**
- Update salary data quarterly
- Monitor industry-specific trends
- Track economic indicators affecting compensation
- Participate in salary surveys

**Dashboard Utilization:**
- Monthly: Review key metrics and trends
- Quarterly: Full benchmark refresh
- Annually: Comprehensive strategy review

### For Job Seekers (Bonus Insights)

#### Maximize Your Market Value:
1. **Invest in High-Value Skills:** IT, data analytics, specialized finance
2. **Target High-Paying Categories:** Technology, banking, healthcare
3. **Build Experience Strategically:** Maximum growth in first 5-7 years
4. **Consider Position Progression:** Move to senior/managerial roles for significant jumps
5. **Negotiate Within Range:** Understand typical salary ranges for your role

## Technologies Used

### Data Analysis
- **Python 3.x** - Core programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Jupyter Notebook** - Interactive analysis environment

### Visualization
- **Matplotlib** - Static plotting
- **Seaborn** - Statistical visualizations
- **Plotly** - Interactive charts and graphs

### Dashboard
- **Streamlit** - Web application framework
- **Plotly Express** - Dashboard visualizations

### Data Processing
- **JSON** - Parsing nested category data
- **Datetime** - Date/time manipulation

## Data Source

**Dataset:** Singapore Job Market Data (MyCareersFuture)
**Time Period:** 2023
**Records:** Multiple job postings with salary information
**Key Fields:**
- Job categories and titles
- Salary ranges (minimum, maximum)
- Position levels
- Years of experience required
- Company information
- Job metadata (views, applications, posting dates)

## Future Enhancements

### Potential Additions:
1. **Predictive Modeling**
   - Salary prediction based on job characteristics
   - Career progression forecasting
   - Market trend predictions

2. **Advanced Filtering**
   - Company size analysis
   - Geographic location comparison
   - Employment type breakdown

3. **Competitive Intelligence**
   - Company-to-company benchmarking
   - Industry vertical analysis
   - Skills premium analysis

4. **Real-time Updates**
   - API integration for live data
   - Automated data refresh
   - Trend alerts

5. **Export Capabilities**
   - Custom report generation
   - PDF export of insights
   - Excel data exports

## Contributing

This project is designed for HR consulting analysis. To contribute or customize:

1. Fork the repository
2. Create analysis branches
3. Add custom visualizations in the notebook
4. Extend dashboard functionality
5. Document new insights

## License

This project is created for educational and consulting purposes. Please ensure compliance with data usage terms from the original data source.

## Contact & Support

For questions, suggestions, or collaboration:
- Review the Jupyter notebook for detailed analysis
- Explore the interactive dashboard for visual insights
- Refer to code comments for technical implementation

---

**Last Updated:** 2025
**Version:** 1.0
**Status:** Production Ready

---

## Quick Start Commands

### Using uv (Recommended)

```bash
# Setup virtual environment and install dependencies
uv venv
source .venv/bin/activate  # macOS/Linux (.venv\Scripts\activate on Windows)
uv pip install -r requirements.txt

# Run Jupyter analysis
jupyter notebook notebooks/salary_analysis.ipynb

# Launch dashboard
cd dashboard && streamlit run app.py
```

### Using pip (Traditional)

```bash
# Install dependencies
pip install -r requirements.txt

# Run Jupyter analysis
jupyter notebook notebooks/salary_analysis.ipynb

# Launch dashboard
cd dashboard && streamlit run app.py
```

## Troubleshooting

### Common Issues:

1. **Module Not Found / Import Errors**
   - **Using uv:** Make sure virtual environment is activated: `source .venv/bin/activate`
   - **Using pip:** Ensure all requirements are installed: `pip install -r requirements.txt`
   - Check Python version: `python --version` (should be 3.8+)
   - Verify you're in the correct virtual environment: `which python` should point to `.venv/bin/python`

2. **Virtual Environment Issues**
   - **uv not found:** Install uv using the installation command in the Installation section
   - **Activation failed:** Make sure you're in the project root directory
   - **Wrong Python version:** Check `uv venv` used the correct Python (shown during creation)
   - **Packages not found after install:** Reactivate the virtual environment

3. **Data Loading Issues**
   - Verify CSV encoding (UTF-8 with BOM)
   - Check file paths are correct
   - Ensure data file exists in `data/` directory

4. **Dashboard Not Loading**
   - Check you're in the dashboard directory when running streamlit
   - Verify port 8501 is not in use
   - Clear browser cache and reload
   - Ensure virtual environment is activated before running streamlit

5. **Visualization Issues**
   - Update plotly: `uv pip install --upgrade plotly` (or `pip install --upgrade plotly`)
   - Restart Jupyter kernel
   - Clear Streamlit cache: Add `?clear_cache=true` to URL

---

## Appendix: Sample Insights

### Example Analysis Output:

```
SINGAPORE JOB MARKET - SALARY BENCHMARKING SUMMARY
================================================================================

1. OVERALL MARKET STATISTICS
   - Total job postings analyzed: 15,000+
   - Median monthly salary: $4,500
   - Mean monthly salary: $5,200
   - Salary range (25th-75th percentile): $3,200 - $6,800

2. TOP 3 HIGHEST PAYING CATEGORIES
   1. Banking / Financial Services: $8,500 median
   2. Information Technology: $7,200 median
   3. Healthcare / Medical: $6,800 median

3. POSITION LEVEL INSIGHTS
   1. Professional: $10,500 median
   2. Manager: $8,000 median
   3. Senior Executive: $6,500 median

4. EXPERIENCE VS SALARY
   - Correlation: 0.52 (moderate positive)
   - Entry level (0 yrs): $3,000 median
   - Mid-level (5 yrs): $5,500 median
   - Senior (10 yrs): $8,200 median
```

---

**Built with care for HR professionals and data enthusiasts**
