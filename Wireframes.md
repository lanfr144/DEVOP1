#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Streamlit Dashboard Wireframes

This document details the user interface layout for the Streamlit data viewer using a Mermaid structural graph.

```mermaid
graph TD
    subgraph Dashboard_Frame ["Streamlit Application Window (XAU Gold Rate Viewer)"]
        direction TB
        
        %% Control Section
        subgraph Controls ["Control Panel (Filters & Actions)"]
            direction LR
            F1["Start Date Selector"]
            F2["End Date Selector"]
            Btn["Refresh Rates Button"]
        end

        %% Chart Visualization Section
        subgraph Visualization ["Data Visualization (Price Trends)"]
            Chart["Interactive Line Chart (Buy vs. Sell Price)"]
        end

        %% Grid Data Section
        subgraph TableSection ["Data Listing (Metrics Table)"]
            Table["Table Grid: Uid | Date | Buy Price | Sell Price"]
        end

        Controls -->|Triggers reload| Visualization
        Visualization -->|Populates dataset| TableSection
    end

    %% Styles
    style Dashboard_Frame fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#f8fafc
    style Controls fill:#1e293b,stroke:#10b981,stroke-width:1px,color:#f8fafc
    style Visualization fill:#1e293b,stroke:#3b82f6,stroke-width:1px,color:#f8fafc
    style TableSection fill:#1e293b,stroke:#718096,stroke-width:1px,color:#f8fafc
```
