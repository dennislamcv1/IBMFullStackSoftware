/*
Copyright 2014 The Kubernetes Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package main

import (
	"bytes"
	"encoding/json"
	"math/rand"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/codegangsta/negroni"
	"github.com/gorilla/mux"
	"github.com/xyproto/simpleredis"
)

var (
	// For when Redis is used
	masterPool *simpleredis.ConnectionPool
	slavePool  *simpleredis.ConnectionPool

	// For when Redis is not used, we just keep it in memory
	lists map[string][]string = map[string][]string{}

	// For Healthz
	startTime time.Time
	delay     float64 = 10 + 5*rand.Float64()
)

type Input struct {
	InputText string `json:"input_text"`
}

type Tone struct {
	ToneName string `json:"tone_name"`
}

func GetList(key string) ([]string, error) {
	// Using Redis
	if slavePool != nil {
		list := simpleredis.NewList(slavePool, key)
		if result, err := list.GetAll(); err == nil {
			return result, err
		}
		// if we can't talk to the slave then assume its not running yet
		// so just try to use the master instead
	}

	// if the slave doesn't exist, read from the master
	if masterPool != nil {
		list := simpleredis.NewList(masterPool, key)
		return list.GetAll()
	}

	// if neither exist, we're probably in "in-memory" mode
	return lists[key], nil
}

func AppendToList(item string, key string) ([]string, error) {
	var err error
	items := []string{}

	// Using Redis
	if masterPool != nil {
		list := simpleredis.NewList(masterPool, key)
		list.Add(item)
		items, err = list.GetAll()
		if err != nil {
			return nil, err
		}
	} else {
		items = lists[key]
		items = append(items, item)
		lists[key] = items
	}
	return items, nil
}

func ListRangeHandler(rw http.ResponseWriter, req *http.Request) {
	var data []byte

	items, err := GetList(mux.Vars(req)["key"])
	if err != nil {
		data = []byte("Error getting list: " + err.Error() + "\n")
	} else {
		if data, err = json.MarshalIndent(items, "", ""); err != nil {
			data = []byte("Error marhsalling list: " + err.Error() + "\n")
		}
	}

	rw.Write(data)
}

func ListPushHandler(rw http.ResponseWriter, req *http.Request) {
	var data []byte

	key := mux.Vars(req)["key"]
	value := mux.Vars(req)["value"]

	// propogate headers to analyzer service
	headers := getForwardHeaders(req.Header)

	// Add in the "tone" analyzer results
	value += " : " + getPrimaryTone(value, headers)

	items, err := AppendToList(value, key)

	if err != nil {
		data = []byte("Error adding to list: " + err.Error() + "\n")
	} else {
		if data, err = json.MarshalIndent(items, "", ""); err != nil {
			data = []byte("Error marshalling list: " + err.Error() + "\n")
		}

	}
	rw.Write(data)
}

func InfoHandler(rw http.ResponseWriter, req *http.Request) {
	info := ""

	// Using Redis
	if masterPool != nil {
		i, err := masterPool.Get(0).Do("INFO")
		if err != nil {
			info = "Error getting DB info: " + err.Error()
		} else {
			info = string(i.([]byte))
		}
	} else {
		info = "In-memory datastore (not redis)"
	}
	rw.Write([]byte(info + "\n"))
}

func EnvHandler(rw http.ResponseWriter, req *http.Request) {
	environment := make(map[string]string)
	for _, item := range os.Environ() {
		splits := strings.Split(item, "=")
		key := splits[0]
		val := strings.Join(splits[1:], "=")
		environment[key] = val
	}

	data, err := json.MarshalIndent(environment, "", "")
	if err != nil {
		data = []byte("Error marshalling env vars: " + err.Error())
	}

	rw.Write(data)
}

func HelloHandler(rw http.ResponseWriter, req *http.Request) {
	rw.Write([]byte("Hello from guestbook. " +
		"Your app is up! (Hostname: " +
		os.Getenv("HOSTNAME") +
		")\n"))
}

func HealthzHandler(rw http.ResponseWriter, req *http.Request) {
	if time.Now().Sub(startTime).Seconds() > delay {
		http.Error(rw, "Timeout, Health check error!", http.StatusForbidden)
	} else {
		rw.Write([]byte("OK!"))
	}
}

// Note: This function will not work until we hook-up the Tone Analyzer service
func getPrimaryTone(value string, headers http.Header) (tone string) {
	u := Input{InputText: value}
	b := new(bytes.Buffer)
	json.NewEncoder(b).Encode(u)

	client := &http.Client{}
	req, err := http.NewRequest("POST", "http://analyzer:80/tone", b)
	if err != nil {
		return "Error talking to tone analyzer service: " + err.Error()
	}
	req.Header.Add("Content-Type", "application/json")
	// add headers
	for k := range headers {
		req.Header.Add(k, headers.Get(k))
	}
	// print out headers for debug
	// fmt.Printf("getPrimaryTone headers %v", req.Header)

	res, err := client.Do(req)
	if err != nil {
		return "Error detecting tone: " + err.Error()
	}
	defer res.Body.Close()

	body := []Tone{}
	json.NewDecoder(res.Body).Decode(&body)
	if len(body) > 0 {
		// 7 tones:  anger, fear, joy, sadness, analytical, confident, and tentative
		if body[0].ToneName == "Joy" {
			return body[0].ToneName + " (✿◠‿◠)"
		} else if body[0].ToneName == "Anger" {
			return body[0].ToneName + " (ಠ_ಠ)"
		} else if body[0].ToneName == "Fear" {
			return body[0].ToneName + " (ง’̀-‘́)ง"
		} else if body[0].ToneName == "Sadness" {
			return body[0].ToneName + " （︶︿︶）"
		} else if body[0].ToneName == "Analytical" {
			return body[0].ToneName + " ( °□° )"
		} else if body[0].ToneName == "Confident" {
			return body[0].ToneName + " (▀̿Ĺ̯▀̿ ̿)"
		} else if body[0].ToneName == "Tentative" {
			return body[0].ToneName + " (•_•)"
		}
		return body[0].ToneName
	}

	return "No Tone Detected"
}

// return the needed header for distributed tracing
func getForwardHeaders(h http.Header) (headers http.Header) {
	incomingHeaders := []string{
		"x-request-id",
		"x-b3-traceid",
		"x-b3-spanid",
		"x-b3-parentspanid",
		"x-b3-sampled",
		"x-b3-flags",
		"x-ot-span-context"}

	header := make(http.Header, len(incomingHeaders))
	for _, element := range incomingHeaders {
		val := h.Get(element)
		if val != "" {
			header.Set(element, val)
		}
	}
	return header
}

// Support multiple URL schemes for different use cases
func findRedisURL() string {
	host := os.Getenv("REDIS_MASTER_SERVICE_HOST")
	port := os.Getenv("REDIS_MASTER_SERVICE_PORT")
	password := os.Getenv("REDIS_MASTER_SERVICE_PASSWORD")
	master_port := os.Getenv("REDIS_MASTER_PORT")

	if host != "" && port != "" && password != "" {
		return password + "@" + host + ":" + port
	} else if master_port != "" {
		return "redis-master:6379"
	}
	return ""
}

func main() {
	// When using Redis, setup our DB connections
	url := findRedisURL()
	if url != "" {
		masterPool = simpleredis.NewConnectionPoolHost(url)
		defer masterPool.Close()
		slavePool = simpleredis.NewConnectionPoolHost("redis-slave:6379")
		defer slavePool.Close()
	}

	startTime = time.Now()

	r := mux.NewRouter()
	r.Path("/lrange/{key}").Methods("GET").HandlerFunc(ListRangeHandler)
	r.Path("/rpush/{key}/{value}").Methods("GET").HandlerFunc(ListPushHandler)
	r.Path("/info").Methods("GET").HandlerFunc(InfoHandler)
	r.Path("/env").Methods("GET").HandlerFunc(EnvHandler)
	r.Path("/hello").Methods("GET").HandlerFunc(HelloHandler)
	r.Path("/healthz").Methods("GET").HandlerFunc(HealthzHandler)

	n := negroni.Classic()
	n.UseHandler(r)
	n.Run(":3000")
}
