using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridManager : MonoBehaviour
{

    private int rows = 5;
    private int columns = 10;

    public static GridManager instance;

    private GameObject[,] squares;
    public List<Sprite> squareSprites = new List<Sprite>();

    private GameObject square;

    // Start is called before the first frame update
    void Start()
    {
        instance = GetComponent<GridManager>();

        GenerateGrid();
    }

    private void GenerateGrid() {
        squares = new GameObject[columns, rows];

        for (int x = 0; x < columns; x++) {
            for (int y = 0; y < rows; y++) {
                float xPosition;
                float yPosition;

                GameObject sq = Instantiate();
            }
        }
    }

    // Update is called once per frame
    void Update()
    {

    }
}
