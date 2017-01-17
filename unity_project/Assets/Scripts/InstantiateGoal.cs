using UnityEngine;
using System.Collections;

public class InstantiateGoal : MonoBehaviour {

    public GameObject goal;

	// Use this for initialization
	void Start () {
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
        float randx = Random.Range(-9.5f, 9.5f);
        float randz = Random.Range(-9.5f, 9.5f);
        GameObject goalClone = (GameObject)Instantiate(goal, new Vector3(randx, 1f, randz), Quaternion.identity);
        goalClone.transform.SetParent(gameObject.transform);
    }
}
