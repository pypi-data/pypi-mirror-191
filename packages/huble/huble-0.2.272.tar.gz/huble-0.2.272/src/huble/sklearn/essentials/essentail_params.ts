export const essentialOptions = [
    {name:"Train-Test Split",
    value:"Train-Test Split",
    parameters:[
      {
        name: "test_size",
        type: "float",
        defaultValue: 0.25,
        render: true,
        optional: true,
      }
      ],
      inputParameters: {
        types: ["Dataframe"],
        isCustomizable: false,
      },
      outputParameters: {
        types: ["Dataframe", "Dataframe"],
        isCustomizable: false,
      },
    },
    {name:"Train Model",
    value:"Train Model",
    parameters:[
        {
            name: "target_column",
            type: "columnName",
            render: true,
            optional: false,
        }
      ],
      inputParameters: {
        types: ["Dataframe", "Model"],
        isCustomizable: false,
      },
      outputParameters: {
        types: ["Model"],
        isCustomizable: false,
      },
    },
]