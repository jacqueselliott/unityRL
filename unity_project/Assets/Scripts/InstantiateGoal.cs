using UnityEngine;
using System.Collections;

public class InstantiateGoal : MonoBehaviour {

    public GameObject goal;
    private float planeSize = 2.5f;
    private GameObject drone;

	// Use this for initialization
	void Start () {
        drone = GameObject.FindGameObjectWithTag("Drone");
        CreateGoal();
	}
	
	// Update is called once per frame
	void Update () {
	    if (gameObject.transform.childCount == 0)
        {
            CreateGoal();
        }
	}

    void CreateGoal()
    {
        float randx = Random.Range(-planeSize+1f, planeSize-1f);
        float randz = Random.Range(-planeSize+1f, planeSize-1f);
        Vector3 spawnLocation = new Vector3(randx, 1f, randz);
		while(Vector3.Distance(spawnLocation, drone.transform.position)<1.5f)
		{
			randx = Random.Range(-planeSize+1f, planeSize-1f);
			randz = Random.Range(-planeSize+1f, planeSize-1f);
			spawnLocation = new Vector3(randx, 1f, randz);
		}
        GameObject goalClone = (GameObject)Instantiate(goal, spawnLocation, Quaternion.identity);
        goalClone.transform.SetParent(gameObject.transform);
    }
}
