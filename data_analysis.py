import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class PharmaDataAnalyzer:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        plt.style.use('default')
        
    def basic_statistics(self):
        """Generate basic statistics"""
        print("=== BASIC STATISTICS ===")
        print(f"Total medicines: {len(self.df)}")
        print(f"Unique medicines: {self.df['medicine_name'].nunique()}")
        print(f"Unique manufacturers: {self.df['marketed_by'].nunique()}")
        print(f"Unique packaging types: {self.df['packagingType'].nunique()}")
        
        # Top manufacturers
        print("\nTop 10 Manufacturers:")
        top_manufacturers = self.df['marketed_by'].value_counts().head(10)
        for i, (manufacturer, count) in enumerate(top_manufacturers.items(), 1):
            print(f"{i}. {manufacturer}: {count} medicines")
    
    def packaging_analysis(self):
        """Analyze packaging types"""
        print("\n=== PACKAGING ANALYSIS ===")
        
        # Most common packaging types
        packaging_counts = self.df['packagingType'].value_counts().head(15)
        print("Top 15 Packaging Types:")
        for i, (pkg, count) in enumerate(packaging_counts.items(), 1):
            print(f"{i}. {pkg}: {count}")
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        packaging_counts.plot(kind='bar')
        plt.title('Top 15 Packaging Types Distribution')
        plt.xlabel('Packaging Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('packaging_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def dosage_analysis(self):
        """Analyze dosage patterns"""
        print("\n=== DOSAGE ANALYSIS ===")
        
        # Extract dosage information
        dosages = []
        for name in self.df['medicine_name']:
            if pd.notna(name):
                # Extract mg dosages
                mg_matches = re.findall(r'(\d+)mg', str(name))
                dosages.extend([int(x) for x in mg_matches])
        
        if dosages:
            dosage_counter = Counter(dosages)
            common_dosages = dosage_counter.most_common(20)
            
            print("Top 20 Common Dosages (mg):")
            for i, (dosage, count) in enumerate(common_dosages, 1):
                print(f"{i}. {dosage}mg: {count} medicines")
            
            # Visualization
            plt.figure(figsize=(12, 6))
            dosages_df = pd.DataFrame(common_dosages, columns=['Dosage (mg)', 'Count'])
            plt.bar(range(len(dosages_df)), dosages_df['Count'])
            plt.xlabel('Dosage (mg)')
            plt.ylabel('Count')
            plt.title('Top 20 Common Dosages Distribution')
            plt.xticks(range(len(dosages_df)), dosages_df['Dosage (mg)'], rotation=45)
            plt.tight_layout()
            plt.savefig('dosage_distribution.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def salt_composition_analysis(self):
        """Analyze salt compositions"""
        print("\n=== SALT COMPOSITION ANALYSIS ===")
        
        # Count number of active ingredients
        ingredient_counts = []
        for composition in self.df['salt_composition']:
            if pd.notna(composition) and composition != 'Not specified':
                count = composition.count('+') + 1
                ingredient_counts.append(count)
        
        if ingredient_counts:
            ingredient_counter = Counter(ingredient_counts)
            print("Distribution of Number of Active Ingredients:")
            for ingredients, count in sorted(ingredient_counter.items()):
                print(f"{ingredients} ingredient(s): {count} medicines")
            
            # Visualization
            plt.figure(figsize=(10, 6))
            ingredients_df = pd.DataFrame(list(ingredient_counter.items()), 
                                        columns=['Number of Ingredients', 'Count'])
            ingredients_df = ingredients_df.sort_values('Number of Ingredients')
            plt.bar(ingredients_df['Number of Ingredients'], ingredients_df['Count'])
            plt.xlabel('Number of Active Ingredients')
            plt.ylabel('Count')
            plt.title('Distribution of Number of Active Ingredients')
            plt.tight_layout()
            plt.savefig('ingredients_distribution.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def gst_analysis(self):
        """Analyze GST information"""
        print("\n=== GST ANALYSIS ===")
        
        # Convert GST to numeric
        gst_numeric = pd.to_numeric(self.df['gst'], errors='coerce')
        gst_available = gst_numeric.dropna()
        
        print(f"Medicines with GST info: {len(gst_available)}")
        print(f"Medicines without GST info: {len(self.df) - len(gst_available)}")
        
        if len(gst_available) > 0:
            print(f"GST rates found: {sorted(gst_available.unique())}")
            
            # GST distribution
            gst_counts = gst_available.value_counts().sort_index()
            print("\nGST Rate Distribution:")
            for rate, count in gst_counts.items():
                print(f"{rate}%: {count} medicines")
            
            # Visualization
            plt.figure(figsize=(10, 6))
            gst_counts.plot(kind='bar')
            plt.title('GST Rate Distribution')
            plt.xlabel('GST Rate (%)')
            plt.ylabel('Count')
            plt.tight_layout()
            plt.savefig('gst_distribution.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def manufacturer_analysis(self):
        """Analyze manufacturer patterns"""
        print("\n=== MANUFACTURER ANALYSIS ===")
        
        # Top manufacturers by product count
        top_manufacturers = self.df['marketed_by'].value_counts().head(20)
        
        print("Top 20 Manufacturers by Product Count:")
        for i, (manufacturer, count) in enumerate(top_manufacturers.items(), 1):
            print(f"{i}. {manufacturer}: {count} products")
        
        # Visualization
        plt.figure(figsize=(15, 8))
        top_manufacturers.plot(kind='barh')
        plt.title('Top 20 Manufacturers by Product Count')
        plt.xlabel('Number of Products')
        plt.ylabel('Manufacturer')
        plt.tight_layout()
        plt.savefig('manufacturer_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_summary_report(self):
        """Create a comprehensive summary report"""
        print("\n" + "="*50)
        print("PHARMACEUTICAL DATASET ANALYSIS SUMMARY")
        print("="*50)
        
        # Basic metrics
        total_medicines = len(self.df)
        unique_medicines = self.df['medicine_name'].nunique()
        unique_manufacturers = self.df['marketed_by'].nunique()
        unique_packaging = self.df['packagingType'].nunique()
        
        # Missing data analysis
        missing_salt = self.df['salt_composition'].isna().sum()
        missing_gst = self.df['gst'].isna().sum()
        missing_manufacturer = self.df['manufactured_by'].isna().sum()
        
        print(f"📊 Dataset Overview:")
        print(f"   • Total medicines: {total_medicines:,}")
        print(f"   • Unique medicines: {unique_medicines:,}")
        print(f"   • Unique manufacturers: {unique_manufacturers:,}")
        print(f"   • Unique packaging types: {unique_packaging}")
        
        print(f"\n🔍 Data Quality:")
        print(f"   • Missing salt composition: {missing_salt:,} ({missing_salt/total_medicines*100:.1f}%)")
        print(f"   • Missing GST info: {missing_gst:,} ({missing_gst/total_medicines*100:.1f}%)")
        print(f"   • Missing manufacturer info: {missing_manufacturer:,} ({missing_manufacturer/total_medicines*100:.1f}%)")
        
        # Top categories
        top_packaging = self.df['packagingType'].value_counts().iloc[0]
        top_manufacturer = self.df['marketed_by'].value_counts().iloc[0]
        
        print(f"\n🏆 Top Categories:")
        print(f"   • Most common packaging: {self.df['packagingType'].value_counts().index[0]} ({top_packaging:,} products)")
        print(f"   • Largest manufacturer: {self.df['marketed_by'].value_counts().index[0]} ({top_manufacturer:,} products)")
        
        print("\n✅ Analysis completed! Check the generated PNG files for visualizations.")

def main():
    # Initialize analyzer
    #analyzer = PharmaDataAnalyzer('c:/Users/LENOVO/Desktop/Projects/CAREECO/Stage1_Product_initial_dataset.csv')

    analyzer = PharmaDataAnalyzer('Stage1_Product_initial_dataset.csv')

    
    # Run all analyses
    analyzer.basic_statistics()
    analyzer.packaging_analysis()
    analyzer.dosage_analysis()
    analyzer.salt_composition_analysis()
    analyzer.gst_analysis()
    analyzer.manufacturer_analysis()
    analyzer.create_summary_report()

if __name__ == "__main__":
    import re
    main()