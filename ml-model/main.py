import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, BayesianRidge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
import streamlit as st

# Streamlit App
st.set_page_config(page_title="Walmart Sales Regression Models", layout="wide")
st.title("Walmart Sales Regression Model Comparison")

# Sidebar for file upload and model selection
st.sidebar.header("Configuration")

uploaded_file = st.sidebar.file_uploader("Upload Walmart_Sales.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

    # Feature Engineering
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df = pd.get_dummies(df, columns=['Store', 'Holiday_Flag'], drop_first=True)

    # Define target and features
    y = np.log(df['Weekly_Sales'])  # Log transform the target variable
    X = df.drop(columns=['Weekly_Sales', 'Date'])

    # Split the dataset into training, validation, and test sets
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    # Model selection
    model_options = [
        'Normal Linear Regression',
        'Multiple Linear Regression',
        'Ridge Regression',
        'Lasso Regression',
        'ElasticNet Regression',
        'Polynomial Regression',
        'Bayesian Ridge Regression'
    ]
    selected_models = st.sidebar.multiselect(
        "Select models to train and compare:", model_options, default=model_options
    )

    # Hyperparameters
    st.sidebar.subheader("Hyperparameters")
    ridge_alpha = st.sidebar.select_slider("Ridge alpha", options=[0.1, 1.0, 10.0, 100.0], value=1.0)
    lasso_alpha = st.sidebar.select_slider("Lasso alpha", options=[0.001, 0.01, 0.1, 0.5, 1.0, 5.0], value=0.1)
    elastic_alpha = st.sidebar.select_slider("ElasticNet alpha", options=[0.01, 0.1, 1.0, 10.0], value=0.1)
    elastic_l1_ratio = st.sidebar.select_slider("ElasticNet l1_ratio", options=[0.1, 0.5, 0.9], value=0.5)
    poly_degree = st.sidebar.select_slider("Polynomial degree", options=[2, 3], value=2)

    results = {}
    plots = {}

    # 1. Normal Linear Regression
    if 'Normal Linear Regression' in selected_models:
        normal_lr = LinearRegression().fit(X_train_scaled, y_train)
        y_val_pred_normal_lr = normal_lr.predict(X_val_scaled)
        y_test_pred_normal_lr = normal_lr.predict(X_test_scaled)
        results['Normal Linear Regression'] = {
            'val_mse': mean_squared_error(y_val, y_val_pred_normal_lr),
            'val_r2': r2_score(y_val, y_val_pred_normal_lr),
            'test_mse': mean_squared_error(y_test, y_test_pred_normal_lr),
            'test_r2': r2_score(y_test, y_test_pred_normal_lr),
            'y_test_pred': y_test_pred_normal_lr
        }

    # 2. Multiple Linear Regression
    if 'Multiple Linear Regression' in selected_models:
        lr = LinearRegression().fit(X_train_scaled, y_train)
        y_val_pred = lr.predict(X_val_scaled)
        y_test_pred = lr.predict(X_test_scaled)
        results['Multiple Linear Regression'] = {
            'val_mse': mean_squared_error(y_val, y_val_pred),
            'val_r2': r2_score(y_val, y_val_pred),
            'test_mse': mean_squared_error(y_test, y_test_pred),
            'test_r2': r2_score(y_test, y_test_pred),
            'y_test_pred': y_test_pred
        }

    # 3. Ridge Regression
    if 'Ridge Regression' in selected_models:
        ridge_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('ridge', Ridge(alpha=ridge_alpha))
        ])
        ridge_pipeline.fit(X_train, y_train)
        y_val_pred_ridge = ridge_pipeline.predict(X_val)
        y_test_pred_ridge = ridge_pipeline.predict(X_test)
        results['Ridge Regression'] = {
            'val_mse': mean_squared_error(y_val, y_val_pred_ridge),
            'val_r2': r2_score(y_val, y_val_pred_ridge),
            'test_mse': mean_squared_error(y_test, y_test_pred_ridge),
            'test_r2': r2_score(y_test, y_test_pred_ridge),
            'y_test_pred': y_test_pred_ridge
        }

    # 4. Lasso Regression
    if 'Lasso Regression' in selected_models:
        lasso_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('lasso', Lasso(alpha=lasso_alpha))
        ])
        lasso_pipeline.fit(X_train, y_train)
        y_val_pred_lasso = lasso_pipeline.predict(X_val)
        y_test_pred_lasso = lasso_pipeline.predict(X_test)
        results['Lasso Regression'] = {
            'val_mse': mean_squared_error(y_val, y_val_pred_lasso),
            'val_r2': r2_score(y_val, y_val_pred_lasso),
            'test_mse': mean_squared_error(y_test, y_test_pred_lasso),
            'test_r2': r2_score(y_test, y_test_pred_lasso),
            'y_test_pred': y_test_pred_lasso
        }

    # 5. ElasticNet Regression
    if 'ElasticNet Regression' in selected_models:
        elastic_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('elastic', ElasticNet(alpha=elastic_alpha, l1_ratio=elastic_l1_ratio))
        ])
        elastic_pipeline.fit(X_train, y_train)
        y_val_pred_elastic = elastic_pipeline.predict(X_val)
        y_test_pred_elastic = elastic_pipeline.predict(X_test)
        results['ElasticNet Regression'] = {
            'val_mse': mean_squared_error(y_val, y_val_pred_elastic),
            'val_r2': r2_score(y_val, y_val_pred_elastic),
            'test_mse': mean_squared_error(y_test, y_test_pred_elastic),
            'test_r2': r2_score(y_test, y_test_pred_elastic),
            'y_test_pred': y_test_pred_elastic
        }

    # 6. Polynomial Regression
    if 'Polynomial Regression' in selected_models:
        poly_pipeline = Pipeline([
            ('poly', PolynomialFeatures(degree=poly_degree)),
            ('scaler', StandardScaler()),
            ('poly_lr', LinearRegression())
        ])
        poly_pipeline.fit(X_train, y_train)
        y_val_pred_poly = poly_pipeline.predict(X_val)
        y_test_pred_poly = poly_pipeline.predict(X_test)
        results['Polynomial Regression'] = {
            'val_mse': mean_squared_error(y_val, y_val_pred_poly),
            'val_r2': r2_score(y_val, y_val_pred_poly),
            'test_mse': mean_squared_error(y_test, y_test_pred_poly),
            'test_r2': r2_score(y_test, y_test_pred_poly),
            'y_test_pred': y_test_pred_poly
        }
        # Residual Plot
        residuals = y_test - y_test_pred_poly
        fig_resid, ax_resid = plt.subplots(figsize=(8, 4))
        sns.residplot(x=y_test_pred_poly, y=residuals, lowess=True, line_kws={'color': 'red', 'lw': 1}, ax=ax_resid)
        ax_resid.set_title('Residual Plot for Polynomial Regression')
        ax_resid.set_xlabel('Predicted Values')
        ax_resid.set_ylabel('Residuals')
        plots['poly_resid'] = fig_resid
        # Predicted vs Actual Plot
        fig_pred, ax_pred = plt.subplots(figsize=(8, 4))
        ax_pred.scatter(y_test, y_test_pred_poly, color='blue', label='Predicted vs Actual')
        ax_pred.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linewidth=2, label='y = x line')
        ax_pred.set_title('Predicted vs Actual Values')
        ax_pred.set_xlabel('Actual Values')
        ax_pred.set_ylabel('Predicted Values')
        ax_pred.legend()
        plots['poly_pred'] = fig_pred

    # 7. Bayesian Ridge Regression
    if 'Bayesian Ridge Regression' in selected_models:
        bayesian_ridge = BayesianRidge().fit(X_train_scaled, y_train)
        y_val_pred_bayesian = bayesian_ridge.predict(X_val_scaled)
        y_test_pred_bayesian = bayesian_ridge.predict(X_test_scaled)
        results['Bayesian Ridge Regression'] = {
            'val_mse': mean_squared_error(y_val, y_val_pred_bayesian),
            'val_r2': r2_score(y_val, y_val_pred_bayesian),
            'test_mse': mean_squared_error(y_test, y_test_pred_bayesian),
            'test_r2': r2_score(y_test, y_test_pred_bayesian),
            'y_test_pred': y_test_pred_bayesian
        }

    # Display Results
    st.subheader("Model Performance on Validation and Test Sets")
    perf_table = []
    for model in selected_models:
        if model in results:
            perf_table.append({
                'Model': model,
                'Validation MSE': results[model]['val_mse'],
                'Validation R²': results[model]['val_r2'],
                'Test MSE': results[model]['test_mse'],
                'Test R²': results[model]['test_r2']
            })
    if perf_table:
        st.dataframe(pd.DataFrame(perf_table).set_index('Model').style.format("{:.4f}"))

    # Model Comparison Plots
    if perf_table:
        mse_values = [row['Test MSE'] for row in perf_table]
        r2_values = [row['Test R²'] for row in perf_table]
        models = [row['Model'] for row in perf_table]
        fig_mse, ax_mse = plt.subplots(figsize=(8, 4))
        ax_mse.barh(models, mse_values, color='skyblue')
        ax_mse.set_title('Model Comparison - MSE (Test Set)')
        ax_mse.set_xlabel('Mean Squared Error')
        ax_mse.set_ylabel('Models')
        st.pyplot(fig_mse)
        fig_r2, ax_r2 = plt.subplots(figsize=(8, 4))
        ax_r2.barh(models, r2_values, color='lightgreen')
        ax_r2.set_title('Model Comparison - R² (Test Set)')
        ax_r2.set_xlabel('R² Score')
        ax_r2.set_ylabel('Models')
        st.pyplot(fig_r2)

    # Show Polynomial Regression Plots if available
    if 'poly_resid' in plots:
        st.subheader("Polynomial Regression Residual Plot")
        st.pyplot(plots['poly_resid'])
    if 'poly_pred' in plots:
        st.subheader("Polynomial Regression: Predicted vs Actual")
        st.pyplot(plots['poly_pred'])
else:
    st.info("Please upload the Walmart_Sales.csv file to begin.")