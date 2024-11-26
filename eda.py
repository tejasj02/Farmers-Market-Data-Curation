import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_preprocess_data(file_path):
    """Load and preprocess market data."""
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['total_population'])
    df = df[df['median_income'] > 0]
    return df

def plot_histograms(df):
    """Plot histograms for total population, median income, and population aged 18-30."""
    plt.figure(figsize=(15, 5))
    for i, col in enumerate(['total_population', 'median_income', 'pop_18_30']):
        plt.subplot(131 + i)
        plt.hist(df[col], bins=30, edgecolor='black')
        plt.title(col.replace('_', ' ').title())
    plt.tight_layout()
    plt.show()

def plot_scatter(df):
    """Plot scatter plot of median income vs. population aged 18-30."""
    plt.figure(figsize=(10, 6))
    plt.scatter(df['median_income'], df['pop_18_30'], s=df['total_population']/1000, alpha=0.5)
    plt.xlabel('Median Income')
    plt.ylabel('Population 18-30')
    plt.title('Income vs. Young Population (size represents total population)')
    plt.colorbar(label='Total Population')
    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(df):
    """Plot a correlation heatmap of the dataset."""
    df_corr = df[['total_population', 'median_income', 'pop_18_30']]
    corr = df_corr.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
    plt.title('Correlation Heatmap of Population Variables')
    plt.tight_layout()
    plt.show()

def print_summary(df):
    """Print summary statistics and information about the dataset."""
    print(f"Original shape: {df.shape}")
    print(f"Missing values:\n{df.isna().sum()}")
    print(f"First few rows:\n{df.head()}")
    
def analyze_zipcodes(df):
    """Analyze the number of unique zipcodes."""
    grouped = df.groupby(by=['zipcode']).sum()
    print(f"Number of unique zipcodes: {len(grouped)}")
    print(f"Total number of rows: {len(df)}")

# Main execution
if __name__ == "__main__":
    data_file = 'market_data.csv'
    
    # Load and preprocess data
    df = load_and_preprocess_data(data_file)
    
    # Plot visualizations
    plot_histograms(df)
    plot_scatter(df)
    
    # Plot correlation heatmap
    plot_correlation_heatmap(df)
    
    # Print summary information
    print_summary(df)
    
    # Analyze zipcodes
    analyze_zipcodes(df)