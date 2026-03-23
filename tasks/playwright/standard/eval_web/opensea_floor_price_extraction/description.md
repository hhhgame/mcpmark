# OpenSea Floor Price Extraction Task

Use Playwright MCP tools to extract NFT rankings from OpenSea and filter collections based on their floor price.

## Requirements:

1. Navigate to https://opensea.io/rankings
2. Ensure the following filters are applied correctly:
   - **Time Range**: Set to "1d" (24 hours)
   - **Chain**: Set to "Ethereum"
3. Extract the ranking list and look for collections that meet the criteria:
   - **Floor Price** must be strictly greater than **1.0 ETH**.
4. Organize the filtered results into CSV format with the following columns:
   - `Collection`: The name of the NFT collection.
   - `Floor Price`: The current floor price as a decimal number (without the "ETH" suffix).
5. Output **ONLY** the complete CSV formatted data wrapped in a markdown code block.

## CSV Data Example:

**The CSV header must exactly match the following (including spaces after commas):**
```csv
Collection, Floor Price
Bored Ape Yacht Club, 5.14
Pudgy Penguins, 4.09
Milady Maker, 1.27
```

## Notes:

- Wait for the rankings table to fully load before extraction.
- Only include collections priced in ETH.
- Do not include any explanations, introduction, or concluding remarks.
- If there are multiple pages or if more content loads on scroll, ensure you capture at least the top 50 matches or as many as possible within the timeout.
- **IMPORTANT: Final output must contain ONLY the CSV code block.**
