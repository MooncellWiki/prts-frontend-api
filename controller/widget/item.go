package widget

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"

	"github.com/labstack/echo/v4"
)

func ItemDemand(c echo.Context) error {
	bytes, err := ioutil.ReadFile("data/item_demand.json")
	if err != nil {
		fmt.Println("An error occurred in file i/o procedure", err)
		return err
	}
	var m map[string]interface{}
	err = json.Unmarshal(bytes, &m)
	if err != nil {
		fmt.Println("Failed to unmarshal json data", err)
		return err
	}

	return c.JSON(http.StatusOK, m[c.Param("itemName")])
}
