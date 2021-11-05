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
		fmt.Println("读取json文件失败", err)
		return err
	}
	var m map[string]interface{}
	err = json.Unmarshal(bytes, &m)
	if err != nil {
		fmt.Println("解析数据失败", err)
		return err
	}

	return c.JSON(http.StatusOK, m[c.Param("itemName")])
}
