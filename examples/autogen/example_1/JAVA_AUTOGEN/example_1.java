import java.io.File;
import java.io.IOException;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties({ "thirty", "moneyIsNotAProblem", "className", "ten" })
public class Person {
    public static final String className = "Person";
    public static final Integer ten = 10;
    public static Integer twelve = null;

    public Boolean isMan = null;

    public Integer age = null;

    public String firstName = null;

    public String lastName = null;

    public final Integer thirty = 30;
    public Boolean moneyIsNotAProblem = null;

    @JsonIgnore
    private final ObjectMapper m_mapper = new ObjectMapper();

    public Boolean getIsMan() {
        return this.isMan;
    }

    public void setIsMan(Boolean isMan) {
        this.isMan = isMan;
    }

    public Integer getAge() {
        return this.age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public String getFirstName() {
        return this.firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return this.lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Integer getThirty() {
        return this.thirty;
    }

    public Boolean getMoneyIsNotAProblem() {
        return this.moneyIsNotAProblem;
    }

    public void setMoneyIsNotAProblem(Boolean moneyIsNotAProblem) {
        this.moneyIsNotAProblem = moneyIsNotAProblem;
    }

    public String toJsonString() throws IOException {
        return this.m_mapper.writerWithDefaultPrettyPrinter().writeValueAsString(this);
    }

    public void saveToJson(String pathToSaveTo) throws IOException {
        this.m_mapper.writerWithDefaultPrettyPrinter().writeValue(new File(pathToSaveTo), this);
    }

    public void fromJsonString(String jsonString) throws IOException {
        Person loaded = this.m_mapper.readValue(jsonString, Person.class);
        this.isMan = loaded.isMan;
        this.age = loaded.age;
        this.firstName = loaded.firstName;
        this.lastName = loaded.lastName;
        
    }

    public void loadFromJson(String pathToLoadFrom) throws IOException {
        Person loaded = this.m_mapper.readValue(new File(pathToLoadFrom), Person.class);
        this.isMan = loaded.isMan;
        this.age = loaded.age;
        this.firstName = loaded.firstName;
        this.lastName = loaded.lastName;
        
    }

    @JsonIgnore
    public String getCategory() {
        return "staff";
    }

    @JsonIgnore
    public String getName() {
        throw new UnsupportedOperationException();
    }
}