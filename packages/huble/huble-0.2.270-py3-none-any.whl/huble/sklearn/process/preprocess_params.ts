export const preprocessingOptions = [
  {name:"Featuretools",
  value:"Featuretools",
  parameters:[
    {
      name: "target_dataframe_name",
      type: "columnList",
      render: true,
    },
    {
      name:"agg_primitives",
      type:"list",
      options:["sum","std","max","skew","min","mean","count","percent_true","n_unique","mode"],
      defaultValue:["sum","std","max"],
      render:true
    },
    {
      name:"trans_primitives",
      type:"list",
      options:["day","month","year","weekday","haversine","num_words","num_characters"],
      defaultValue:["day","month","year","weekday","haversine","num_words","num_characters"],
      render:true
    },
    {
      name:"max_depth",
      type:"number",
      defaultValue:2,
      render:true
    }
    ],
  },
  {
    name: "Custom function",
    value: "custom",
    parameters:[
      {
        name: "code",
        type: "code",
        defaultValue: "def custom_function(df):\n\treturn df",
        render: true,
      }
    ],

  },
  {
    name: "Remove NAN values",
    value: "Remove NAN values",
    parameters: [
      {
        name: "axis",
        type: "select",
        options: [0, 1],
        defaultValue: 0,
        render: true,
        optional: true,
      },
      {
        name: "how",
        type: "select",
        options: ["any", "all"],
        defaultValue: "any",
        render: true,
        optional: true,
      },
      {
        name: "subset",
        type: "columnList",
        render: true,
        optional: true,
      },
      {
        name: "inplace",
        type: "bool",
        options: [true, false],
        defaultValue: false,
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe","Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    //add iterative imputer

    name: "Replace NAN values",
    value: "Replace NAN values",
    parameters: [
      {
        name: "column",
        type: "columnName",
        render: true,
        optional: false,
      },
      {
        name: "missing_values",
        type: "any", //int | number | str | np.nan| None |pandas.NA
        defaultValue: "np.nan",
        render: true,
        optional: true,
      },
      {
        name: "strategy",
        type: "select",
        options: ["mean", "median", "most_frequent", "constant"],
        defaultValue: "mean",
        render: true,
        optional: false,
      },
      {
        name: "fill_value", //for 'constant' strategy
        type: "string", //Also can be a number
        defaultValue: "None",
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Dropping rows or columns",
    value: "Dropping rows or columns",
    parameters: [
      {
        name: "labels",
        type: "columnList",
        render: true,
        optional: false,
      },
      {
        name: "axis",
        type: "select",
        options: [0, 1],
        defaultValue: 1,
        render: true,
        optional: true,
      },
      {
        name: "inplace",
        type: "bool",
        options: [true, false],
        defaultValue: false,
        render: true,
        optional: true,
      },
      {
        name: "errors",
        type: "select",
        options: ["ignore", "raise"],
        defaultValue: "raise",
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Remove Outliers",
    value: "Remove Outliers",
    parameters: [
      {
        name: "columns",
        type: "columnList",
        render: true,
        optional: false,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Drop Duplicates",
    value: "Drop Duplicates",
    parameters: [
      {
        name: "subset",
        type: "columnList",
        render: true,
        optional: true,
      },
      {
        name: "keep",
        type: "select",
        options: ["first", "last", false],
        defaultValue: "first",
        render: true,
        optional: true,
      },
      {
        name: "inplace",
        type: "bool",
        options: [true, false],
        defaultValue: false,
        render: true,
        optional: true,
      },
      {
        name: "ignore_index",
        type: "bool",
        options: [true, false],
        defaultValue: false,
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Change Data Type",
    value: "Change Data Type",
    parameters: [
      {
        name: "column",
        type: "columnName",
        render: true,
        optional: false,
      },
      {
        name: "data type",
        type: "string",
        render: true,
        optional: false,
      },
      {
        name: "copy",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
      {
        name: "errors",
        type: "select",
        options: ["raise", "ignore"],
        defaultValue: "raise",
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Round Data",
    value: "Round Data",
    parameters: [
      {
        name: "decimals",
        type: "dict",
        render: true,
        optional: false,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Filter Dataframe",
    value: "Filter Dataframe",
    parameters: [
      {
        name: "items",
        type: "list",
        render: true,
        optional: true,
      },
      {
        name: "like",
        type: "string",
        render: true,
        optional: true,
      },
      {
        name: "axis",
        type: "select",
        options: [0, 1, "None"],
        defaultValue: "None",
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Truncate Dataframe",
    value: "Truncate Dataframe",
    parameters: [
      {
        name: "before",
        type: "any", //date | str | int (column name or index)
        render: true,
        optional: false,
      },
      {
        name: "after",
        type: "any", //date | str | int (column name or index)
        render: true,
        optional: false,
      },
      {
        name: "axis",
        type: "select",
        options: [0, 1, "None"],
        defaultValue: "None",
        render: true,
        optional: false,
      },
      {
        name: "copy",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Sort Values",
    value: "Sort Values",
    parameters: [
      {
        name: "by",
        type: "columnList",
        render: true,
        optional: false,
      },
      {
        name: "ascending",
        type: "select",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
      {
        name: "axis",
        type: "select",
        options: [0, 1],
        defaultValue: 0,
        render: true,
        optional: true,
      },
      {
        name: "inplace",
        type: "bool",
        options: [true, false],
        defaultValue: false,
        render: true,
        optional: true,
      },
      {
        name: "kind",
        type: "select",
        options: ["quicksort", "mergesort", "heapsort", "stable"],
        defaultValue: "quicksort",
        render: true,
        optional: true,
      },
      {
        name: "na_position",
        type: "select",
        options: ["first", "last"],
        defaultValue: "last",
        render: true,
        optional: true,
      },
      {
        name: "ignore_index",
        type: "bool",
        options: [true, false],
        defaultValue: false,
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Transpose Dataframe",
    value: "Transpose Dataframe",
    parameters: [],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Min Max Scaler",
    value: "Min Max Scaler",
    parameters: [
      {
        name: "columns",
        type: "columnList",
        render: true,
        optional: false,
      },
      {
        name: "feature_range",
        type: "tuple", //(min,max)
        defaultValue: "(0, 1)",
        render: true,
        optional: true,
      },
      {
        name: "copy",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
      {
        name: "clip",
        type: "bool",
        options: [true, false],
        defaultValue: false,
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Max Abs Scaler",
    value: "Max Abs Scaler",
    parameters: [
      {
        name: "columns",
        type: "columnList",
        render: true,
        optional: false,
      },
      {
        name: "copy",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Robust Scaler",
    value: "Robust Scaler",
    parameters: [
      {
        name: "column",
        type: "columnName",
        render: true,
        optional: false,
      },
      {
        name: "with_centering",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
      {
        name: "with_scaling",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
      {
        name: "copy",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
      {
        name: "unit_variance",
        type: "bool",
        options: [true, false],
        defaultValue: false,
        render: true,
        optional: true,
      },
      {
        name: "quantile_range",
        type: "tuple",
        defaultValue: "(25.0,75.0)",
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Standard Scaler",
    value: "Standard Scaler",
    parameters: [
      {
        name: "column",
        type: "columnName",
        render: true,
        optional: false,
      },
      {
        name: "copy",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
      {
        name: "with_mean",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
      {
        name: "with_std",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Normalization",
    value: "Normalization",
    parameters: [
      {
        name: "column",
        type: "columnList",
        render: true,
        optional: false,
      },
      {
        name: "norm",
        type: "select",
        options: ["l1", "l2", "max"],
        defaultValue: "l2",
        render: true,
        optional: true,
      },
      {
        name: "copy",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Ordinal Encoding",
    value: "Ordinal Encoding",
    parameters: [
      {
        name: "columns",
        type: "columnList",
        render: true,
        optional: false,
      },
      {
        name: "categories",
        type: "list", //or auto
        defaultValue: "auto",
        render: true,
        optional: true,
      },
      {
        name: "dtype",
        type: "str",
        defaultValue: "np.number64",
        render: true,
        optional: true,
      },
      {
        name: "handle_unknown",
        type: "select",
        options: ["error", "use_encoded_value"],
        defaultValue: "error",
        render: true,
        optional: true,
      },
      {
        name: "unknown_value", //for 'use_encoded_value'
        type: "int", //int | np.nan
        defaultValue: "None",
        render: true,
        optional: true,
      },
      {
        name: "encoded_missing_value",
        type: "int", //int | np.nan
        defaultValue: "np.nan",
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "One Hot Encoding",
    value: "One Hot Encoding",
    parameters: [
      {
        name: "columns",
        type: "columnList",
        render: true,
        optional: false,
      },
      {
        name: "categories",
        type: "list", //or auto
        defaultValue: "auto",
        render: true,
        optional: true,
      },
      {
        name: "dtype",
        type: "str",
        defaultValue: "np.number",
        render: true,
        optional: true,
      },
      {
        name: "handle_unknown",
        type: "select",
        options: ["error", "ignore", "infrequent_if_exist"],
        defaultValue: "error",
        render: true,
        optional: true,
      },
      {
        name: "sparse",
        type: "bool",
        options: [true, false],
        defaultValue: true,
        render: true,
        optional: true,
      },
      {
        name: "min_frequency",
        type: "number",
        defaultValue: "None",
        render: true,
        optional: true,
      },
      {
        name: "max_categories",
        type: "number",
        defaultValue: "None",
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Remove Mismatch Data",
    value: "Remove Mismatch Data",
    parameters: [
      {
        name: "exceptions",
        type: "columnList",
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Rename Columns",
    value: "Rename Columns",
    parameters: [
      {
        name: "mapper",
        type: "dict", //or function
        render: true,
        optional: false,
      },
      {
        name: "axis",
        type: "select",
        options: [0,1],
        defaultValue: 0,
        render: true,
        optional: true,
      },
      {
        name: "errors",
        type: "select",
        options: ['raise', 'ignore'],
        defaultValue: 'ignore',
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Select Columns",
    value: "Select Columns",  //check
    parameters: [
      {
        name: "include",
        type: "columnList",
        render: true,
        optional: true,
      },
      {
        name: "exclude",
        type: "columnList",
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Clean Column Names",
    value: "Clean Column Names",
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Clip",
    value: "Clip",
    parameters: [
      {
        name: "lower",
        type: "number",
        defaultValue: 'None',
        render: true,
        optional: true,
      },
      {
        name: "upper",
        type: "number",
        defaultValue: 'None',
        render: true,
        optional: true,
      },
      {
        name: "axis",
        type: "select",
        options: [0, 1],
        defaultValue: 'None',
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Merge Datasets",
    value: "Merge Datasets",
    parameters: [
      {
        name: "right",
        type: "dataFrame",
        render: true,
        optional: false,
      },
      {
        name: "how",
        type: "select",
        options: ["right", "left", "inner", "outer", "cross"],
        defaultValue: "inner",
        render: true,
        optional: true,
      },
      {
        name: "on",
        type: "columnList",
        render: true,
        optional: true,
      },
      {
        name: "left_on",
        type: "columnList",
        render: true,
        optional: true,
      },
      {
        name: "right_on",
        type: "columnList",
        render: true,
        optional: true,
      },
      {
        name: "sort",
        type: "select",
        options: [true, false],
        defaultValue: false,
        render: true,
        optional: true,
      },
    ],
    inputParameters: {
      types: ["Dataframe","Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Split Datasets", 
    value: "Split Datasets",
    parameters: [     
    ],
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe","Dataframe"],
      isCustomizable: false,
    },
  },
  {
    name: "Clean Dataset",
    value: "Clean Dataset",
    inputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
    outputParameters: {
      types: ["Dataframe"],
      isCustomizable: false,
    },
  },
];
